#!/usr/bin/env bash
set -euo pipefail

JENKINS_URL="${JENKINS_URL:-http://localhost:8080}"

# 1. Worker payload script
cat << 'WORKER_EOF' > /tmp/worker_payload.sh
#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo "  LESSON 9 WORKER: AUDIT & METADATA GENERATOR"
echo "=========================================================="

TARGET_ENV="${TARGET_ENV:-staging}"
REQUEST_ID="${REQUEST_ID:-unknown}"
FORCE_FAIL="${FORCE_FAIL:-false}"

echo "--> Environment : ${TARGET_ENV}"
echo "--> Request ID  : ${REQUEST_ID}"
echo "--> Force Fail  : ${FORCE_FAIL}"
echo "--> Node Name   : ${NODE_NAME:-built-in}"

if [ "${FORCE_FAIL}" = "true" ]; then
    echo "[ERROR] Simulated failure triggered via FORCE_FAIL=true!"
    exit 1
fi

cat << JSON_EOF > audit_report.json
{
  "request_id": "${REQUEST_ID}",
  "environment": "${TARGET_ENV}",
  "worker_build": "${BUILD_NUMBER}",
  "executed_on": "${NODE_NAME:-built-in}",
  "checks_passed": true
}
JSON_EOF

if command -v sha256sum >/dev/null 2>&1; then
    sha256sum audit_report.json > audit_report.sha256
else
    shasum -a 256 audit_report.json > audit_report.sha256
fi

echo "[SUCCESS] audit_report.json and audit_report.sha256 generated in ${WORKSPACE}"
WORKER_EOF

B64_WORKER=$(base64 < /tmp/worker_payload.sh | tr -d '\n')

cat << GROOVY_WORKER_EOF > /tmp/provision_lesson9_worker.groovy
import jenkins.model.Jenkins
import hudson.model.FreeStyleProject
import hudson.model.ParametersDefinitionProperty
import hudson.model.StringParameterDefinition
import hudson.model.ChoiceParameterDefinition
import hudson.model.BooleanParameterDefinition
import hudson.model.labels.LabelAtom
import hudson.tasks.Shell
import hudson.tasks.ArtifactArchiver

def instance = Jenkins.get()
def jobName = 'lesson9-audit-worker'

def job = instance.getItem(jobName) ?: instance.createProject(FreeStyleProject, jobName)
job.setAssignedLabel(new LabelAtom('built-in'))

job.removeProperty(ParametersDefinitionProperty.class)
def envParam = new ChoiceParameterDefinition('TARGET_ENV', ['dev', 'staging', 'prod'] as String[], 'Target deployment environment')
def reqParam = new StringParameterDefinition('REQUEST_ID', 'REQ-000', 'Tracking ID from upstream orchestrator')
def failParam = new BooleanParameterDefinition('FORCE_FAIL', false, 'Simulate a worker crash for testing')
job.addProperty(new ParametersDefinitionProperty(envParam, reqParam, failParam))

String decodedScript = new String("${B64_WORKER}".decodeBase64())
job.getBuildersList().clear()
job.getBuildersList().add(new Shell(decodedScript))

job.getPublishersList().clear()
job.getPublishersList().add(new ArtifactArchiver('audit_report.json,audit_report.sha256'))

job.save()
println "LESSON9_WORKER_READY"
GROOVY_WORKER_EOF

curl -s -X POST "${JENKINS_URL}/scriptText" --data-urlencode "script@/tmp/provision_lesson9_worker.groovy"

# 2. Orchestrator payload script (pure grep/cut parser, no python needed)
cat << 'ORCH_EOF' > /tmp/orchestrator_payload.sh
#!/usr/bin/env bash
set -euo pipefail

JENKINS_URL="${JENKINS_URL:-http://localhost:8080}"
CHILD_JOB="lesson9-audit-worker"
ENV_CHOICE="${TARGET_ENV:-staging}"
SIMULATE_FAIL="${FORCE_FAIL:-false}"
TRACKING_ID="ORD-${BUILD_NUMBER:-local}-$(date +%s)"

echo "=========================================================="
echo "  LESSON 9 ORCHESTRATOR (BUILD #${BUILD_NUMBER:-local})"
echo "=========================================================="

HEADER_FILE="/tmp/headers_${BUILD_NUMBER:-local}.txt"
QUEUE_FILE="/tmp/queue_${BUILD_NUMBER:-local}.json"
BUILD_FILE="/tmp/build_${BUILD_NUMBER:-local}.json"

TRIGGER_URL="${JENKINS_URL}/job/${CHILD_JOB}/buildWithParameters?TARGET_ENV=${ENV_CHOICE}&REQUEST_ID=${TRACKING_ID}&FORCE_FAIL=${SIMULATE_FAIL}"
curl -s -D "${HEADER_FILE}" -o /dev/null -X POST "${TRIGGER_URL}"

HTTP_STATUS=$(grep -i "^HTTP/" "${HEADER_FILE}" | tail -n 1 | awk '{print $2}' | tr -d '\r\n')
QUEUE_URL=$(grep -i "^Location:" "${HEADER_FILE}" | awk '{print $2}' | tr -d '\r\n')

if [ "${HTTP_STATUS}" != "201" ] || [ -z "${QUEUE_URL}" ]; then
    echo "[ERROR] Trigger failed! HTTP Status: ${HTTP_STATUS}"
    exit 1
fi

QUEUE_URL="${QUEUE_URL%/}/"
QUEUE_ID=$(echo "${QUEUE_URL}" | awk -F'/' '{for(i=NF;i>0;i--) if($i!="") {print $i; break}}')
echo "--> Queue Item Created: ${QUEUE_URL} (id=${QUEUE_ID})"

CHILD_BUILD_NUM=""
WAIT_SECONDS=0
MAX_QUEUE_WAIT=30

while [ -z "${CHILD_BUILD_NUM}" ]; do
    if [ "${WAIT_SECONDS}" -ge "${MAX_QUEUE_WAIT}" ]; then
        echo "[ERROR] Timed out waiting in queue after ${MAX_QUEUE_WAIT}s."
        exit 1
    fi

    HTTP_CODE=$(curl -s -o "${QUEUE_FILE}" -w "%{http_code}" "${QUEUE_URL}api/json" || echo "000")

    if [ "${HTTP_CODE}" = "200" ] && [ -s "${QUEUE_FILE}" ]; then
        if grep -q '"cancelled":true' "${QUEUE_FILE}"; then
            echo "[ERROR] Downstream job was cancelled while in queue!"
            exit 1
        fi

        # Extract executable number using grep/cut
        CHILD_BUILD_NUM=$(grep -A 5 '"executable":' "${QUEUE_FILE}" 2>/dev/null | grep -o '"number":[0-9]*' | head -n 1 | cut -d: -f2 | tr -d '[:space:]' || true)
    fi

    # Fallback: check recent builds of downstream job if queue item left
    if [ -z "${CHILD_BUILD_NUM}" ]; then
        curl -s "${JENKINS_URL}/job/${CHILD_JOB}/api/json?tree=builds[number,queueId]" -o "${BUILD_FILE}" || true
        if [ -s "${BUILD_FILE}" ]; then
            CHILD_BUILD_NUM=$(grep -B 1 -A 2 "\"queueId\":${QUEUE_ID}" "${BUILD_FILE}" 2>/dev/null | grep -o '"number":[0-9]*' | head -n 1 | cut -d: -f2 | tr -d '[:space:]' || true)
            if [ -z "${CHILD_BUILD_NUM}" ]; then
                CHILD_BUILD_NUM=$(grep -o '"number":[0-9]*' "${BUILD_FILE}" 2>/dev/null | head -n 1 | cut -d: -f2 | tr -d '[:space:]' || true)
            fi
        fi
    fi

    if [ -z "${CHILD_BUILD_NUM}" ]; then
        sleep 1
        WAIT_SECONDS=$((WAIT_SECONDS + 1))
    fi
done

echo "--> Executor Assigned! Child Build #${CHILD_BUILD_NUM} is active."

while true; do
    curl -s "${JENKINS_URL}/job/${CHILD_JOB}/${CHILD_BUILD_NUM}/api/json" -o "${BUILD_FILE}" || true
    if [ -s "${BUILD_FILE}" ]; then
        IS_BUILDING=$(grep -o '"building":[^,}]*' "${BUILD_FILE}" 2>/dev/null | head -n 1 | cut -d: -f2 | tr -d '[:space:]' || echo "true")

        if [ "${IS_BUILDING}" = "false" ]; then
            BUILD_RESULT=$(grep -o '"result":[^,}]*' "${BUILD_FILE}" 2>/dev/null | head -n 1 | cut -d: -f2 | tr -d '[:space:]"' || echo "UNKNOWN")
            echo "--> Child Build #${CHILD_BUILD_NUM} Finished with Result: ${BUILD_RESULT}"
            break
        fi
    fi
    sleep 2
done

if [ "${BUILD_RESULT}" != "SUCCESS" ]; then
    echo "[ERROR] Downstream job failed (${BUILD_RESULT}). Aborting parent pipeline."
    exit 1
fi

ARTIFACT_BASE="${JENKINS_URL}/job/${CHILD_JOB}/${CHILD_BUILD_NUM}/artifact"
curl -s -f -o "audit_report.json" "${ARTIFACT_BASE}/audit_report.json"
curl -s -f -o "audit_report.sha256" "${ARTIFACT_BASE}/audit_report.sha256"

echo "--> Verifying SHA-256 checksum of audit_report.json..."
if command -v sha256sum >/dev/null 2>&1; then
    sha256sum -c audit_report.sha256
else
    shasum -a 256 -c audit_report.sha256
fi

cp -f audit_report.json ingested_audit.json
echo "[SUCCESS] SHA-256 verification passed and report ingested!"
ORCH_EOF

B64_ORCH=$(base64 < /tmp/orchestrator_payload.sh | tr -d '\n')

cat << GROOVY_PARENT_EOF > /tmp/provision_lesson9_parent.groovy
import jenkins.model.Jenkins
import hudson.model.FreeStyleProject
import hudson.model.ParametersDefinitionProperty
import hudson.model.ChoiceParameterDefinition
import hudson.model.BooleanParameterDefinition
import hudson.model.labels.LabelAtom
import hudson.tasks.Shell

def instance = Jenkins.get()
def jobName = 'lesson9-orchestrator'

def job = instance.getItem(jobName) ?: instance.createProject(FreeStyleProject, jobName)
job.setAssignedLabel(new LabelAtom('built-in'))

job.removeProperty(ParametersDefinitionProperty.class)
def envParam = new ChoiceParameterDefinition('TARGET_ENV', ['dev', 'staging', 'prod'] as String[], 'Environment to audit')
def failParam = new BooleanParameterDefinition('FORCE_FAIL', false, 'Pass failure flag to downstream worker')
job.addProperty(new ParametersDefinitionProperty(envParam, failParam))

String decodedScript = new String("${B64_ORCH}".decodeBase64())
job.getBuildersList().clear()
job.getBuildersList().add(new Shell(decodedScript))

job.save()
println "LESSON9_PARENT_READY"
GROOVY_PARENT_EOF

curl -s -X POST "${JENKINS_URL}/scriptText" --data-urlencode "script@/tmp/provision_lesson9_parent.groovy"
