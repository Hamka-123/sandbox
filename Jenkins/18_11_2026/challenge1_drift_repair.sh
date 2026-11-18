#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -euo pipefail

# Jenkins base URL (override via JENKINS_URL if needed)
JENKINS_URL="${JENKINS_URL:-http://localhost:8080}"
JOB_NAME="drift-target-job"
ARTIFACT_FILE="tier.txt"
EXPECTED_TIER="staging"

# Desired-state Groovy snippet (idempotent)
read -r -d '' DESIRED_STATE_GROOVY << 'EOF' || true
import jenkins.model.Jenkins
import hudson.model.FreeStyleProject
import hudson.model.StringParameterDefinition
import hudson.model.ParametersDefinitionProperty
import hudson.tasks.Shell
import hudson.tasks.ArtifactArchiver

def jobName = "drift-target-job"
def jenkins = Jenkins.get()
def job = jenkins.getItem(jobName)

if (job == null) {
    println "Creating job: ${jobName}"
    job = jenkins.createProject(FreeStyleProject.class, jobName)
} else {
    println "Updating job in place: ${jobName}"
}

def paramsProp = new ParametersDefinitionProperty(
    new StringParameterDefinition("ENV_TIER", "staging", "Target environment tier")
)
job.removeProperty(ParametersDefinitionProperty.class)
job.addProperty(paramsProp)

job.getBuildersList().clear()
def shellBuilder = new Shell('''rm -f tier.txt
echo "tier=\${ENV_TIER}" > tier.txt''')
job.getBuildersList().add(shellBuilder)

job.getPublishersList().clear()
def archiver = new ArtifactArchiver("tier.txt")
archiver.setOnlyIfSuccessful(true)
job.getPublishersList().add(archiver)

job.save()
println "Desired state applied for ${jobName} (ENV_TIER=staging, onlyIfSuccessful=true)."
EOF

# Drift-simulation Groovy snippet (simulates manual UI corruption)
read -r -d '' DRIFT_GROOVY << 'EOF' || true
import jenkins.model.Jenkins
import hudson.model.FreeStyleProject
import hudson.model.StringParameterDefinition
import hudson.model.ParametersDefinitionProperty
import hudson.tasks.ArtifactArchiver

def jobName = "drift-target-job"
def jenkins = Jenkins.get()
def job = jenkins.getItem(jobName)

if (job == null) {
    throw new IllegalStateException("Job ${jobName} does not exist to simulate drift.")
}

def driftedParams = new ParametersDefinitionProperty(
    new StringParameterDefinition("ENV_TIER", "broken-dev", "Drifted environment tier")
)
job.removeProperty(ParametersDefinitionProperty.class)
job.addProperty(driftedParams)

job.getPublishersList().clear()
def driftedArchiver = new ArtifactArchiver("tier.txt")
driftedArchiver.setOnlyIfSuccessful(false)
job.getPublishersList().add(driftedArchiver)

job.save()
println "Simulated manual UI drift on ${jobName}: ENV_TIER='broken-dev', onlyIfSuccessful=false."
EOF

echo "=== Step 1: Bootstrap ${JOB_NAME} ==="
curl -sS -X POST "${JENKINS_URL}/scriptText" \
  --data-urlencode "script=${DESIRED_STATE_GROOVY}"

echo "=== Step 2: Simulate Manual UI Drift ==="
curl -sS -X POST "${JENKINS_URL}/scriptText" \
  --data-urlencode "script=${DRIFT_GROOVY}"

echo "=== Step 3a: Audit via REST API ==="
AUDIT_URL="${JENKINS_URL}/job/${JOB_NAME}/api/json?tree=property[parameterDefinitions[name,defaultParameterValue[value]]]"
AUDIT_JSON=$(curl -sS -g "${AUDIT_URL}")

# Extract ENV_TIER default value across nested JSON objects using grep, sed, and awk
CURRENT_DEFAULT=$(echo "${AUDIT_JSON}" \
  | grep -o '"defaultParameterValue":{[^}]*},"name":"ENV_TIER"\|"name":"ENV_TIER"[^}]*"defaultParameterValue":{[^}]*}' \
  | grep -o '"value":"[^"]*"' \
  | sed 's/^"value":"//; s/"$//' \
  | awk 'NR==1 { print $0 }' || true)

echo "Comparing ENV_TIER default: actual='${CURRENT_DEFAULT:-<none>}' vs expected='${EXPECTED_TIER}'"

if [ "${CURRENT_DEFAULT}" != "${EXPECTED_TIER}" ]; then
    echo "MISMATCH: '${CURRENT_DEFAULT:-<none>}' != '${EXPECTED_TIER}' -> Drift detected! Re-applying desired state..."
    curl -sS -X POST "${JENKINS_URL}/scriptText" \
      --data-urlencode "script=${DESIRED_STATE_GROOVY}"
else
    echo "MATCH: '${CURRENT_DEFAULT}' == '${EXPECTED_TIER}' -> No drift detected."
fi

echo "=== Step 3b: Trigger Default Build via Location: ==="
HEADERS_FILE="$(mktemp)"
trap 'rm -f "${HEADERS_FILE}" "${ARTIFACT_FILE}"' EXIT

curl -sS -D "${HEADERS_FILE}" -o /dev/null -X POST \
  "${JENKINS_URL}/job/${JOB_NAME}/buildWithParameters?delay=0sec" \
  --data-urlencode "ENV_TIER=staging"

QUEUE_URL=$(grep -i '^Location:' "${HEADERS_FILE}" \
  | sed -e 's/^Location:[[:space:]]*//' -e 's/[[:space:]]*\r$//' \
  | head -n 1)

if [ -z "${QUEUE_URL}" ]; then
    echo "ERROR: Missing Location header from buildWithParameters." >&2
    exit 1
fi
QUEUE_URL="${QUEUE_URL%/}/"
echo "Queue item URL: ${QUEUE_URL}"

BUILD_NUM=""
ATTEMPTS=0
MAX_ATTEMPTS=30
while [ -z "${BUILD_NUM}" ]; do
    ATTEMPTS=$((ATTEMPTS + 1))
    if [ "${ATTEMPTS}" -gt "${MAX_ATTEMPTS}" ]; then
        echo "ERROR: Timed out waiting for build number from ${QUEUE_URL}." >&2
        exit 1
    fi

    CODE=$(curl -sS -g -o /dev/null -w "%{http_code}" "${QUEUE_URL}api/json?tree=executable[number]")
    if [ "${CODE}" = "404" ]; then
        FALLBACK_NUM=$(curl -sS -g "${JENKINS_URL}/job/${JOB_NAME}/api/json?tree=builds[number]" \
          | grep -o '"number":[0-9]*' | head -n 1 | sed 's/"number"://' || true)
        if [ -n "${FALLBACK_NUM}" ]; then
            BUILD_NUM="${FALLBACK_NUM}"
            echo "Resolved build #${BUILD_NUM} via fast-eviction fallback."
            break
        fi
    elif [ "${CODE}" = "200" ]; then
        EXEC_JSON=$(curl -sS -g "${QUEUE_URL}api/json?tree=executable[number]")
        NUM=$(echo "${EXEC_JSON}" \
          | grep -o '"executable"[[:space:]]*:[[:space:]]*{[^}]*}' \
          | grep -o '"number"[[:space:]]*:[[:space:]]*[0-9]*' \
          | grep -o '[0-9]*' | head -n 1 || true)
        if [ -n "${NUM}" ]; then
            BUILD_NUM="${NUM}"
            echo "Pinned to build #${BUILD_NUM}."
            break
        fi
    fi
    sleep 1
done

echo "=== Step 3c: Wait for Build #${BUILD_NUM} Completion ==="
BUILD_RESULT=""
while true; do
    BUILD_JSON=$(curl -sS -g "${JENKINS_URL}/job/${JOB_NAME}/${BUILD_NUM}/api/json?tree=building,result")
    BUILDING=$(echo "${BUILD_JSON}" | grep -o '"building":[^,}]*' | sed 's/"building"://')
    if [ "${BUILDING}" = "false" ]; then
        BUILD_RESULT=$(echo "${BUILD_JSON}" | grep -o '"result":"[^"]*"' | sed 's/"result"://; s/"//g' || true)
        echo "Build #${BUILD_NUM} finished with result: ${BUILD_RESULT:-UNKNOWN}"
        break
    fi
    sleep 1
done

if [ "${BUILD_RESULT}" != "SUCCESS" ]; then
    echo "ERROR: Build #${BUILD_NUM} did not succeed (result=${BUILD_RESULT})." >&2
    exit 1
fi

echo "=== Step 3d: Verify Downloaded ${ARTIFACT_FILE} ==="
curl -f -sS -o "${ARTIFACT_FILE}" "${JENKINS_URL}/job/${JOB_NAME}/${BUILD_NUM}/artifact/${ARTIFACT_FILE}"

EXPECTED_LINE="tier=${EXPECTED_TIER}"
ACTUAL_CONTENT=$(cat "${ARTIFACT_FILE}")

echo "Comparing artifact content: actual='${ACTUAL_CONTENT}' vs expected='${EXPECTED_LINE}'"

if [ "${ACTUAL_CONTENT}" = "${EXPECTED_LINE}" ]; then
    echo "SUCCESS: '${ACTUAL_CONTENT}' == '${EXPECTED_LINE}'."
else
    echo "ERROR: '${ACTUAL_CONTENT}' != '${EXPECTED_LINE}'." >&2
    exit 1
fi