#!/usr/bin/env bash
set -euo pipefail

JENKINS_URL="http://localhost:8080"
JOB_NAME="payment-batch-worker"
NODE_URL="${JENKINS_URL}/computer/(built-in)"

echo "============================================================"
echo "  CHALLENGE 1: FLEET CAPACITY & ADMISSION CONTROLLER"
echo "============================================================"
echo "Target job     : ${JOB_NAME}"
echo "Admission rule : reject new batch if queued items >= 2"
echo ""

echo "=== 1. Bootstrap Job from Scratch ==="
echo "[STEP 1.1] Provisioning Freestyle job '${JOB_NAME}' via Groovy /scriptText..."
curl -s -f -X POST "${JENKINS_URL}/scriptText" \
  --data-urlencode "script=
import jenkins.model.Jenkins
import hudson.model.FreeStyleProject
import hudson.model.ParametersDefinitionProperty
import hudson.model.StringParameterDefinition
import hudson.tasks.Shell
import hudson.tasks.ArtifactArchiver

def j = Jenkins.get()
def job = j.getItem('${JOB_NAME}') ?: j.createProject(FreeStyleProject, '${JOB_NAME}')

job.removeProperty(ParametersDefinitionProperty.class)
def batchParam = new StringParameterDefinition('BATCH_ID', 'BATCH-DEFAULT', 'Batch identifier')
job.addProperty(new ParametersDefinitionProperty(batchParam))

def cmd = '''#!/usr/bin/env bash
set -euo pipefail
echo \"[WORKER] Starting batch \${BATCH_ID:-BATCH-DEFAULT} on node \${NODE_NAME:-built-in}...\"
sleep 4
echo \"BATCH_ID=\${BATCH_ID:-BATCH-DEFAULT}\" > batch.receipt
echo \"[WORKER] Finished batch \${BATCH_ID:-BATCH-DEFAULT} and wrote batch.receipt:\"
cat batch.receipt
'''

job.getBuildersList().clear()
job.getBuildersList().add(new Shell(cmd))

job.getPublishersList().clear()
def archiver = new ArtifactArchiver('batch.receipt')
archiver.setOnlyIfSuccessful(true)
job.getPublishersList().add(archiver)

job.save()
println 'BOOTSTRAP_READY: ${JOB_NAME}'
"

BEFORE_COUNT=$(curl -s -f -g "${JENKINS_URL}/job/${JOB_NAME}/api/json?tree=builds[number]" \
  | grep -o '"number":[0-9]*' | wc -l | tr -d ' ' || true)
echo "[STEP 1.2] Baseline builds in '${JOB_NAME}' before traffic burst: ${BEFORE_COUNT}"

echo ""
echo "=== 2. Simulate Traffic Burst (BATCH-1, BATCH-2, BATCH-3) ==="
WAS_OFFLINE=$(curl -s -f -g "${NODE_URL}/api/json?tree=temporarilyOffline" \
  | sed -n 's/.*"temporarilyOffline":\([a-z]*\).*/\1/p')

if [ "${WAS_OFFLINE}" != "true" ]; then
    echo "[STEP 2.1] Temporarily cordoning built-in node so burst items accumulate in queue..."
    curl -s -f -X POST "${NODE_URL}/toggleOffline?offlineMessage=Burst%20queue%20accumulation" > /dev/null
else
    echo "[STEP 2.1] Built-in node was already offline."
fi

QUEUE_ITEMS=""
for BATCH_ID in "BATCH-1" "BATCH-2" "BATCH-3"; do
    HEADERS=$(curl -s -f -D - -o /dev/null -X POST \
      "${JENKINS_URL}/job/${JOB_NAME}/buildWithParameters?delay=0sec&BATCH_ID=${BATCH_ID}")
    Q_URL=$(echo "${HEADERS}" | grep -i "^Location:" | head -n 1 | cut -d' ' -f2- | tr -d '\r\n ')
    QUEUE_ITEMS="${QUEUE_ITEMS} ${BATCH_ID}:${Q_URL}"
    echo "  -> Enqueued ${BATCH_ID} | Queue item URL: ${Q_URL}"
done

if [ "${WAS_OFFLINE}" != "true" ]; then
    echo "[STEP 2.2] Releasing built-in node back to online (items remain in queue until executors pick them up)..."
    curl -s -f -X POST "${NODE_URL}/toggleOffline" > /dev/null
fi

echo ""
echo "=== 3. Admission Control Gate Before BATCH-4 ==="
echo "[STEP 3.1] Inspecting /queue/api/json before accepting BATCH-4..."
QUEUE_JSON=$(curl -s -f -g "${JENKINS_URL}/queue/api/json?tree=items[id,task[name]]")
QUEUE_COUNT=$(echo "${QUEUE_JSON}" | grep -o '"id":[0-9]*' | wc -l | tr -d ' ' || true)
echo "  -> Queue snapshot : ${QUEUE_JSON}"
echo "  -> Queued count   : ${QUEUE_COUNT} (threshold: >= 2)"

if [ "${QUEUE_COUNT}" -ge 2 ]; then
    echo "[ADMISSION DENIED] Queue saturation threshold reached (${QUEUE_COUNT} items waiting)"
    echo "  -> BATCH-4 was NOT dispatched to protect queue latency and executor stability."
else
    echo "[ERROR] Expected at least 2 items in queue, got ${QUEUE_COUNT}"
    exit 1
fi

echo ""
echo "=== 4. Drain & Verify Build Count ==="
echo "[STEP 4.1] Resolving queue items to concrete build numbers..."
TRIGGERED_BUILDS=""
for ENTRY in ${QUEUE_ITEMS}; do
    BATCH_ID="${ENTRY%%:*}"
    Q_URL="${ENTRY#*:}"
    B_NUM=""
    while [ -z "${B_NUM}" ]; do
        Q_JSON=$(curl -s -g "${Q_URL}api/json?tree=executable[number],cancelled" || true)
        B_NUM=$(echo "${Q_JSON}" | sed -n 's/.*"number":\([0-9]*\).*/\1/p')
        [ -z "${B_NUM}" ] && sleep 0.2
    done
    TRIGGERED_BUILDS="${TRIGGERED_BUILDS} ${BATCH_ID}#${B_NUM}"
    echo "  -> ${BATCH_ID} pinned to build #${B_NUM}"
done

echo "[STEP 4.2] Waiting for all accepted builds to complete and checking artifacts..."
for ITEM in ${TRIGGERED_BUILDS}; do
    BATCH_ID="${ITEM%%#*}"
    B_NUM="${ITEM##*#}"
    while true; do
        B_JSON=$(curl -s -f -g "${JENKINS_URL}/job/${JOB_NAME}/${B_NUM}/api/json?tree=building,result")
        BUILDING=$(echo "${B_JSON}" | sed -n 's/.*"building":\([a-z]*\).*/\1/p')
        if [ "${BUILDING}" = "false" ]; then
            RESULT=$(echo "${B_JSON}" | sed -n 's/.*"result":"\([^"]*\)".*/\1/p')
            RECEIPT=$(curl -s -f "${JENKINS_URL}/job/${JOB_NAME}/${B_NUM}/artifact/batch.receipt" | tr -d '\r')
            echo "  -> ${BATCH_ID} (Build #${B_NUM}): result=${RESULT} | artifact=[${RECEIPT}]"
            if [ "${RESULT}" != "SUCCESS" ]; then
                echo "[ERROR] Build #${B_NUM} failed with ${RESULT}"
                exit 1
            fi
            break
        fi
        sleep 1
    done
done

AFTER_COUNT=$(curl -s -f -g "${JENKINS_URL}/job/${JOB_NAME}/api/json?tree=builds[number]" \
  | grep -o '"number":[0-9]*' | wc -l | tr -d ' ' || true)
NEW_BUILDS=$((AFTER_COUNT - BEFORE_COUNT))

echo ""
echo "[STEP 4.3] Final build count check:"
echo "  -> Builds before burst : ${BEFORE_COUNT}"
echo "  -> Builds after burst  : ${AFTER_COUNT}"
echo "  -> New builds created  : ${NEW_BUILDS} (expected <= 3)"

if [ "${NEW_BUILDS}" -gt 3 ]; then
    echo "[ERROR] Expected at most 3 new builds, got ${NEW_BUILDS}"
    exit 1
fi

echo ""
echo "[SUCCESS] Challenge 1 passed completely! Admission control blocked overflow cleanly."
