#!/usr/bin/env bash
set -euo pipefail

JENKINS_URL="http://localhost:8080"
DEGRADED_NODE="pool-node-1"
WORKER_JOB="pool-health-worker"
POOL_LABEL="worker-pool"

echo "============================================================"
echo "  CHALLENGE 2: DEGRADED-NODE QUARANTINE & REBALANCE"
echo "============================================================"
echo "Degraded node : ${DEGRADED_NODE}"
echo "Pool label    : ${POOL_LABEL}"
echo "Worker job    : ${WORKER_JOB}"
echo ""

echo "=== 1. Bootstrap Fleet & Job from Scratch ==="
echo "[STEP 1.1] Configuring '${POOL_LABEL}' on built-in node, registering '${DEGRADED_NODE}', and provisioning '${WORKER_JOB}'..."
curl -s -f -X POST "${JENKINS_URL}/scriptText" \
  --data-urlencode "script=
import jenkins.model.Jenkins
import hudson.slaves.DumbSlave
import hudson.slaves.JNLPLauncher
import hudson.model.Node
import hudson.model.FreeStyleProject
import hudson.tasks.Shell
import hudson.tasks.ArtifactArchiver

def j = Jenkins.get()

// 1. Ensure built-in node carries worker-pool label
j.setLabelString('${POOL_LABEL}')
println '  -> Built-in node label set to: ${POOL_LABEL}'

// 2. Register or update virtual agent pool-node-1
def existingNode = j.getNode('${DEGRADED_NODE}')
if (existingNode == null) {
    def agent = new DumbSlave(
        '${DEGRADED_NODE}',
        '/tmp/jenkins-agent-pool1',
        new JNLPLauncher(true)
    )
    agent.setNumExecutors(1)
    agent.setMode(Node.Mode.NORMAL)
    agent.setLabelString('${POOL_LABEL}')
    j.addNode(agent)
    println '  -> CREATED_NODE: ${DEGRADED_NODE} (executors=1, mode=NORMAL, label=${POOL_LABEL})'
} else {
    existingNode.setNumExecutors(1)
    existingNode.setMode(Node.Mode.NORMAL)
    existingNode.setLabelString('${POOL_LABEL}')
    println '  -> UPDATED_NODE: ${DEGRADED_NODE} (executors=1, mode=NORMAL, label=${POOL_LABEL})'
}

// 3. Create or update pool-health-worker bound to worker-pool
def job = j.getItem('${WORKER_JOB}') ?: j.createProject(FreeStyleProject, '${WORKER_JOB}')
job.setAssignedLabel(j.getLabel('${POOL_LABEL}'))

def cmd = '''#!/usr/bin/env bash
set -euo pipefail
ACTUAL_NODE=\"\${NODE_NAME:-built-in}\"
echo \"[WORKER] Running on node: \${ACTUAL_NODE}\"
echo \"EXECUTED_NODE=\${ACTUAL_NODE}\" > placement.txt
cat placement.txt
'''

job.getBuildersList().clear()
job.getBuildersList().add(new Shell(cmd))

job.getPublishersList().clear()
def archiver = new ArtifactArchiver('placement.txt')
archiver.setOnlyIfSuccessful(true)
job.getPublishersList().add(archiver)

job.save()
j.save()
println '  -> BOOTSTRAP_READY: job=${WORKER_JOB} bound to label=${POOL_LABEL}'
"

echo ""
echo "=== 2. Quarantine Degraded Node (${DEGRADED_NODE}) ==="
echo "[STEP 2.1] Checking current offline state of '${DEGRADED_NODE}' via REST API..."
NODE_STATE=$(curl -s -f -g "${JENKINS_URL}/computer/${DEGRADED_NODE}/api/json?tree=temporarilyOffline,offlineCauseReason")
echo "  -> State before quarantine : ${NODE_STATE}"

if echo "${NODE_STATE}" | grep -q '"temporarilyOffline":false'; then
    echo "[STEP 2.2] Cordoning '${DEGRADED_NODE}' with reason 'Degraded Node Quarantined'..."
    curl -s -f -X POST \
      "${JENKINS_URL}/computer/${DEGRADED_NODE}/toggleOffline?offlineMessage=Degraded%20Node%20Quarantined" > /dev/null
else
    echo "[STEP 2.2] '${DEGRADED_NODE}' is already marked temporarilyOffline."
fi

AFTER_QUARANTINE=$(curl -s -f -g "${JENKINS_URL}/computer/${DEGRADED_NODE}/api/json?tree=temporarilyOffline,offlineCauseReason")
echo "  -> State after quarantine  : ${AFTER_QUARANTINE}"
echo "${AFTER_QUARANTINE}" | grep -q '"temporarilyOffline":true'
echo "${AFTER_QUARANTINE}" | grep -q "Degraded Node Quarantined"
echo "  -> Verified: '${DEGRADED_NODE}' is quarantined and excluded from scheduling."

echo ""
echo "=== 3. Execute & Verify Rebalanced Routing ==="
echo "[STEP 3.1] Dispatching '${WORKER_JOB}' (label=${POOL_LABEL}) with delay=0sec..."
HEADERS=$(curl -s -f -D - -o /dev/null -X POST "${JENKINS_URL}/job/${WORKER_JOB}/build?delay=0sec")
Q_URL=$(echo "${HEADERS}" | grep -i "^Location:" | head -n 1 | cut -d' ' -f2- | tr -d '\r\n ')
echo "  -> Queue item URL : [${Q_URL}]"
if [ -z "${Q_URL}" ]; then
    echo "[ERROR] Failed to capture Location header"
    exit 1
fi

echo "[STEP 3.2] Polling queue until concrete build number is assigned..."
BUILD_NUM=""
while [ -z "${BUILD_NUM}" ]; do
    sleep 1
    Q_JSON=$(curl -s -g "${Q_URL}api/json?tree=executable[number],cancelled" || true)
    if echo "${Q_JSON}" | grep -q '"cancelled":true'; then
        echo "[ERROR] Queue item was cancelled"
        exit 1
    fi
    BUILD_NUM=$(echo "${Q_JSON}" | sed -n 's/.*"number":\([0-9]*\).*/\1/p')
done
echo "  -> Pinned to build #${BUILD_NUM}"

echo "[STEP 3.3] Waiting for build #${BUILD_NUM} to finish..."
while true; do
    B_JSON=$(curl -s -f -g "${JENKINS_URL}/job/${WORKER_JOB}/${BUILD_NUM}/api/json?tree=building,result")
    BUILDING=$(echo "${B_JSON}" | sed -n 's/.*"building":\([a-z]*\).*/\1/p')
    if [ "${BUILDING}" = "false" ]; then
        RESULT=$(echo "${B_JSON}" | sed -n 's/.*"result":"\([^"]*\)".*/\1/p')
        break
    fi
    sleep 1
done

echo "  -> Build #${BUILD_NUM} finished with result: ${RESULT}"
if [ "${RESULT}" != "SUCCESS" ]; then
    echo "[ERROR] Expected SUCCESS, got ${RESULT}"
    exit 1
fi

echo "[STEP 3.4] Downloading 'placement.txt' artifact and verifying rebalanced node..."
curl -s -f -o "placement.txt" "${JENKINS_URL}/job/${WORKER_JOB}/${BUILD_NUM}/artifact/placement.txt"
PLACEMENT_CONTENT=$(cat placement.txt | tr -d '\r')
echo "  -> Artifact placement.txt : [${PLACEMENT_CONTENT}]"
echo "${PLACEMENT_CONTENT}" | grep -q "EXECUTED_NODE=built-in"
echo "  -> Verified: build routed around quarantined '${DEGRADED_NODE}' and ran on 'built-in'."

echo ""
echo "=== 4. Cleanup Hygiene ==="
CURRENT_OFFLINE=$(curl -s -f -g "${JENKINS_URL}/computer/${DEGRADED_NODE}/api/json?tree=temporarilyOffline" \
  | sed -n 's/.*"temporarilyOffline":\([a-z]*\).*/\1/p' || true)
if [ "${CURRENT_OFFLINE}" = "true" ]; then
    echo "[STEP 4.1] Uncordoning '${DEGRADED_NODE}' before removal..."
    curl -s -f -X POST "${JENKINS_URL}/computer/${DEGRADED_NODE}/toggleOffline" > /dev/null
fi

echo "[STEP 4.2] Removing '${DEGRADED_NODE}' via Groovy if idle..."
CLEANUP_OUT=$(curl -s -f -X POST "${JENKINS_URL}/scriptText" \
  --data-urlencode "script=
import jenkins.model.Jenkins

def j = Jenkins.get()
def node = j.getNode('${DEGRADED_NODE}')
if (node != null && node.toComputer()?.isIdle()) {
    j.removeNode(node)
    j.save()
    println '  -> REMOVED_NODE: ${DEGRADED_NODE}'
} else {
    println '  -> NODE_NOT_PRESENT_OR_BUSY: ${DEGRADED_NODE}'
}
")
echo "${CLEANUP_OUT}"

echo ""
echo "[SUCCESS] Challenge 2 passed completely! Quarantined node was bypassed and cleaned up."
