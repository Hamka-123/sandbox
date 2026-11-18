#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -euo pipefail

# Jenkins base URL (override via JENKINS_URL if needed)
JENKINS_URL="${JENKINS_URL:-http://localhost:8080}"
AUTH_JOB="svc-auth-check"
BILLING_JOB="svc-billing-check"
AUTH_ARTIFACT="auth.txt"
BILLING_ARTIFACT="billing.txt"

# Temporary files cleanup on exit
HEADERS_AUTH="$(mktemp)"
HEADERS_BILLING="$(mktemp)"
trap 'rm -f "${HEADERS_AUTH}" "${HEADERS_BILLING}" "${AUTH_ARTIFACT}" "${BILLING_ARTIFACT}"' EXIT

# Step 1: Zero-Dependency Setup via POST /scriptText
read -r -d '' SETUP_GROOVY << 'EOF' || true
import jenkins.model.Jenkins
import hudson.model.FreeStyleProject
import hudson.model.StringParameterDefinition
import hudson.model.ParametersDefinitionProperty
import hudson.tasks.Shell
import hudson.tasks.ArtifactArchiver

def provisionServiceJob(String jobName, int sleepSeconds, String prefix, String artifactFile) {
    def jenkins = Jenkins.get()
    def job = jenkins.getItem(jobName)

    if (job == null) {
        println "Creating job from scratch: ${jobName}"
        job = jenkins.createProject(FreeStyleProject.class, jobName)
    } else {
        println "Updating existing job in place: ${jobName}"
    }

    def params = new ParametersDefinitionProperty(
        new StringParameterDefinition("CORR_ID", "", "Correlation ID for fan-out release check")
    )
    job.removeProperty(ParametersDefinitionProperty.class)
    job.addProperty(params)

    job.getBuildersList().clear()
    def scriptBody = """rm -f ${artifactFile}
sleep ${sleepSeconds}
echo "${prefix}:\${CORR_ID}" > ${artifactFile}"""
    job.getBuildersList().add(new Shell(scriptBody))

    job.getPublishersList().clear()
    def archiver = new ArtifactArchiver(artifactFile)
    archiver.setOnlyIfSuccessful(true)
    job.getPublishersList().add(archiver)

    job.save()
    println "Provisioned and saved ${jobName} (sleep=${sleepSeconds}s, artifact=${artifactFile})."
}

provisionServiceJob("svc-auth-check", 2, "AUTH_OK", "auth.txt")
provisionServiceJob("svc-billing-check", 3, "BILLING_OK", "billing.txt")
EOF

echo "=== Step 1: Zero-Dependency Setup ==="
curl -sS -X POST "${JENKINS_URL}/scriptText" \
  --data-urlencode "script=${SETUP_GROOVY}"

# Step 2: Concurrent Fan-Out
CORR_ID="FAN-$(date +%s)"
echo "=== Step 2: Concurrent Fan-Out (CORR_ID=${CORR_ID}) ==="

curl -sS -D "${HEADERS_AUTH}" -o /dev/null -X POST \
  "${JENKINS_URL}/job/${AUTH_JOB}/buildWithParameters?delay=0sec" \
  --data-urlencode "CORR_ID=${CORR_ID}"

curl -sS -D "${HEADERS_BILLING}" -o /dev/null -X POST \
  "${JENKINS_URL}/job/${BILLING_JOB}/buildWithParameters?delay=0sec" \
  --data-urlencode "CORR_ID=${CORR_ID}"

QUEUE_AUTH=$(grep -i '^Location:' "${HEADERS_AUTH}" \
  | sed -e 's/^Location:[[:space:]]*//' -e 's/[[:space:]]*\r$//' \
  | head -n 1)

QUEUE_BILLING=$(grep -i '^Location:' "${HEADERS_BILLING}" \
  | sed -e 's/^Location:[[:space:]]*//' -e 's/[[:space:]]*\r$//' \
  | head -n 1)

if [ -z "${QUEUE_AUTH}" ] || [ -z "${QUEUE_BILLING}" ]; then
    echo "ERROR: Failed to capture Location headers for both jobs." >&2
    exit 1
fi

QUEUE_AUTH="${QUEUE_AUTH%/}/"
QUEUE_BILLING="${QUEUE_BILLING%/}/"
echo "Dispatched ${AUTH_JOB} -> ${QUEUE_AUTH}"
echo "Dispatched ${BILLING_JOB} -> ${QUEUE_BILLING}"

# Helper function to resolve a queue URL to a concrete build number
resolve_build_number() {
    local queue_url="$1"
    local job_name="$2"
    local build_num=""
    local attempts=0
    local max_attempts=30

    while [ -z "${build_num}" ]; do
        attempts=$((attempts + 1))
        if [ "${attempts}" -gt "${max_attempts}" ]; then
            echo "ERROR: Timed out resolving build number for ${job_name} (${queue_url})." >&2
            return 1
        fi

        local code
        code=$(curl -sS -g -o /dev/null -w "%{http_code}" "${queue_url}api/json?tree=executable[number]")

        if [ "${code}" = "404" ]; then
            # Fast-eviction fallback
            local fallback
            fallback=$(curl -sS -g "${JENKINS_URL}/job/${job_name}/api/json?tree=builds[number]" \
              | grep -o '"number"[[:space:]]*:[[:space:]]*[0-9]*' \
              | head -n 1 \
              | grep -o '[0-9]*' || true)
            if [ -n "${fallback}" ]; then
                build_num="${fallback}"
                break
            fi
        elif [ "${code}" = "200" ]; then
            local exec_json
            exec_json=$(curl -sS -g "${queue_url}api/json?tree=executable[number]")
            local num
            num=$(echo "${exec_json}" \
              | grep -o '"executable"[[:space:]]*:[[:space:]]*{[^}]*}' \
              | grep -o '"number"[[:space:]]*:[[:space:]]*[0-9]*' \
              | grep -o '[0-9]*' \
              | head -n 1 || true)
            if [ -n "${num}" ]; then
                build_num="${num}"
                break
            fi
        fi
        sleep 1
    done

    echo "${build_num}"
}

# Helper function to poll a build until building == false and return its result
wait_for_build() {
    local job_name="$1"
    local build_num="$2"
    local attempts=0
    local max_attempts=60

    while true; do
        attempts=$((attempts + 1))
        if [ "${attempts}" -gt "${max_attempts}" ]; then
            echo "ERROR: Timed out waiting for ${job_name} #${build_num} to finish." >&2
            return 1
        fi

        local build_json
        build_json=$(curl -sS -g "${JENKINS_URL}/job/${job_name}/${build_num}/api/json?tree=building,result")
        local building
        building=$(echo "${build_json}" | grep -o '"building"[[:space:]]*:[[:space:]]*[^,}]*' | sed 's/.*:[[:space:]]*//')

        if [ "${building}" = "false" ]; then
            local result
            result=$(echo "${build_json}" | grep -o '"result"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*:[[:space:]]*"//; s/"$//' || true)
            echo "${result:-UNKNOWN}"
            return 0
        fi
        sleep 1
    done
}

# Step 3: Dual Queue Resolution & Polling
echo "=== Step 3: Dual Queue Resolution & Polling ==="
BUILD_AUTH=$(resolve_build_number "${QUEUE_AUTH}" "${AUTH_JOB}")
BUILD_BILLING=$(resolve_build_number "${QUEUE_BILLING}" "${BILLING_JOB}")
echo "Resolved build numbers -> ${AUTH_JOB}: #${BUILD_AUTH}, ${BILLING_JOB}: #${BUILD_BILLING}"

RESULT_AUTH=$(wait_for_build "${AUTH_JOB}" "${BUILD_AUTH}")
RESULT_BILLING=$(wait_for_build "${BILLING_JOB}" "${BUILD_BILLING}")
echo "Completed results -> ${AUTH_JOB} #${BUILD_AUTH}: ${RESULT_AUTH}, ${BILLING_JOB} #${BUILD_BILLING}: ${RESULT_BILLING}"

if [ "${RESULT_AUTH}" != "SUCCESS" ] || [ "${RESULT_BILLING}" != "SUCCESS" ]; then
    echo "RELEASE VERDICT: FAILED (one or more validation jobs did not succeed)." >&2
    exit 1
fi

# Step 4: Unified Contract Report
echo "=== Step 4: Unified Contract Report ==="
curl -f -sS -o "${AUTH_ARTIFACT}" "${JENKINS_URL}/job/${AUTH_JOB}/${BUILD_AUTH}/artifact/${AUTH_ARTIFACT}"
curl -f -sS -o "${BILLING_ARTIFACT}" "${JENKINS_URL}/job/${BILLING_JOB}/${BUILD_BILLING}/artifact/${BILLING_ARTIFACT}"

AUTH_CONTENT=$(cat "${AUTH_ARTIFACT}")
BILLING_CONTENT=$(cat "${BILLING_ARTIFACT}")

EXPECTED_AUTH="AUTH_OK:${CORR_ID}"
EXPECTED_BILLING="BILLING_OK:${CORR_ID}"

if [ "${AUTH_CONTENT}" != "${EXPECTED_AUTH}" ]; then
    echo "ERROR: ${AUTH_ARTIFACT} mismatch! Expected '${EXPECTED_AUTH}', got '${AUTH_CONTENT}'." >&2
    exit 1
fi

if [ "${BILLING_CONTENT}" != "${EXPECTED_BILLING}" ]; then
    echo "ERROR: ${BILLING_ARTIFACT} mismatch! Expected '${EXPECTED_BILLING}', got '${BILLING_CONTENT}'." >&2
    exit 1
fi

DURATION_AUTH=$(curl -sS -g "${JENKINS_URL}/job/${AUTH_JOB}/${BUILD_AUTH}/api/json?tree=duration" \
  | grep -o '"duration"[[:space:]]*:[[:space:]]*[0-9]*' \
  | grep -o '[0-9]*' | head -n 1 || echo "0")

DURATION_BILLING=$(curl -sS -g "${JENKINS_URL}/job/${BILLING_JOB}/${BUILD_BILLING}/api/json?tree=duration" \
  | grep -o '"duration"[[:space:]]*:[[:space:]]*[0-9]*' \
  | grep -o '[0-9]*' | head -n 1 || echo "0")

echo "============================================================"
echo "             UNIFIED RELEASE CONTRACT REPORT                "
echo "============================================================"
echo "Correlation ID : ${CORR_ID}"
echo "Verdict        : RELEASE APPROVED (ALL CHECKS PASSED)"
echo "------------------------------------------------------------"
echo "Service 1      : ${AUTH_JOB}"
echo "  Build Number : #${BUILD_AUTH}"
echo "  Status       : ${RESULT_AUTH}"
echo "  Duration     : ${DURATION_AUTH} ms"
echo "  Artifact     : ${AUTH_ARTIFACT} -> '${AUTH_CONTENT}'"
echo "------------------------------------------------------------"
echo "Service 2      : ${BILLING_JOB}"
echo "  Build Number : #${BUILD_BILLING}"
echo "  Status       : ${RESULT_BILLING}"
echo "  Duration     : ${DURATION_BILLING} ms"
echo "  Artifact     : ${BILLING_ARTIFACT} -> '${BILLING_CONTENT}'"
echo "============================================================"