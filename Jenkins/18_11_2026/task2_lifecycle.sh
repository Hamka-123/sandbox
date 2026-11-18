#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -euo pipefail

# Jenkins base URL (override via JENKINS_URL if needed)
JENKINS_URL="${JENKINS_URL:-http://localhost:8080}"
JOB_NAME="lab-runner-check"
OUT_FILE="token.out"

# Step 1: Self-Contained Setup via POST /scriptText
read -r -d '' GROOVY_SCRIPT << 'EOF' || true
import jenkins.model.Jenkins
import hudson.model.FreeStyleProject
import hudson.model.StringParameterDefinition
import hudson.model.ParametersDefinitionProperty
import hudson.tasks.Shell
import hudson.tasks.ArtifactArchiver

def jobName = "lab-runner-check"
def jenkins = Jenkins.get()
def job = jenkins.getItem(jobName)

if (job == null) {
    println "Creating job: ${jobName}"
    job = jenkins.createProject(FreeStyleProject.class, jobName)
} else {
    println "Updating existing job in place: ${jobName}"
}

def params = new ParametersDefinitionProperty(
    new StringParameterDefinition("TOKEN", "", "Execution token")
)
job.removeProperty(ParametersDefinitionProperty.class)
job.addProperty(params)

job.getBuildersList().clear()
def shellStep = new Shell('''rm -f token.out
sleep 2
echo "TOKEN=\${TOKEN}" > token.out''')
job.getBuildersList().add(shellStep)

job.getPublishersList().clear()
def archiver = new ArtifactArchiver("token.out")
archiver.setOnlyIfSuccessful(true)
job.getPublishersList().add(archiver)

job.save()
println "Provisioned and saved job: ${jobName}"
EOF

echo "=== Step 1: Provisioning ${JOB_NAME} ==="
curl -sS -X POST "${JENKINS_URL}/scriptText" \
  --data-urlencode "script=${GROOVY_SCRIPT}"

# Step 2: Immediate Queue Dispatch with delay=0sec and dynamic TOKEN
TOKEN_VAL="TOK-$(date +%s)"
echo "=== Step 2: Dispatching build with TOKEN=${TOKEN_VAL} and delay=0sec ==="

HEADERS_FILE="$(mktemp)"
trap 'rm -f "${HEADERS_FILE}" "${OUT_FILE}"' EXIT

curl -sS -D "${HEADERS_FILE}" -o /dev/null -X POST \
  "${JENKINS_URL}/job/${JOB_NAME}/buildWithParameters?delay=0sec" \
  --data-urlencode "TOKEN=${TOKEN_VAL}"

# Step 3: Deterministic Queue-to-Build Pinning via Location header
QUEUE_URL=$(grep -i '^Location:' "${HEADERS_FILE}" | sed -e 's/^Location:[[:space:]]*//' -e 's/[[:space:]]*\r$//' | head -n 1)
if [ -z "${QUEUE_URL}" ]; then
    echo "ERROR: Failed to capture Location header from buildWithParameters response." >&2
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
        echo "ERROR: Timed out waiting for executable build number from ${QUEUE_URL}" >&2
        exit 1
    fi

    CODE=$(curl -sS -g -o /dev/null -w "%{http_code}" "${QUEUE_URL}api/json?tree=executable[number]")
    if [ "${CODE}" = "404" ]; then
        FALLBACK_NUM=$(curl -sS -g "${JENKINS_URL}/job/${JOB_NAME}/api/json?tree=builds[number]" \
          | grep -o '"number":[0-9]*' | head -n 1 | sed 's/"number"://' || true)
        if [ -n "${FALLBACK_NUM}" ]; then
            BUILD_NUM="${FALLBACK_NUM}"
            echo "Queue item returned 404 (fast eviction); resolved build #${BUILD_NUM}"
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
            echo "Pinned to build #${BUILD_NUM}"
            break
        fi
    fi
    sleep 1
done

# Step 4: Polling Until Completion (building == false)
echo "=== Step 4: Polling build #${BUILD_NUM} until completion ==="
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

# Step 5: Round-Trip Artifact Verification
echo "=== Step 5: Downloading and verifying ${OUT_FILE} for build #${BUILD_NUM} ==="
curl -f -sS -o "${OUT_FILE}" "${JENKINS_URL}/job/${JOB_NAME}/${BUILD_NUM}/artifact/${OUT_FILE}"

EXPECTED_LINE="TOKEN=${TOKEN_VAL}"
ACTUAL_CONTENT=$(cat "${OUT_FILE}")

if [ "${ACTUAL_CONTENT}" = "${EXPECTED_LINE}" ]; then
    echo "SUCCESS: ${OUT_FILE} matches '${EXPECTED_LINE}'"
else
    echo "ERROR: Artifact mismatch! Expected '${EXPECTED_LINE}', got '${ACTUAL_CONTENT}'" >&2
    exit 1
fi