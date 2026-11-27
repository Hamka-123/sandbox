#!/usr/bin/env bash
set -euo pipefail

JENKINS_URL="http://localhost:8080"
NODE_NAME="pt1-ephemeral-node"

register_node() {
    curl -s -f -X POST "${JENKINS_URL}/scriptText" \
      --data-urlencode "script=
import jenkins.model.Jenkins
import hudson.slaves.DumbSlave
import hudson.slaves.JNLPLauncher
import hudson.model.Node

def j = Jenkins.get()
def name = '${NODE_NAME}'

if (j.getNode(name) == null) {
    def agent = new DumbSlave(
        name,
        '/tmp/jenkins-agent-pt1',
        new JNLPLauncher(true)
    )
    agent.setNumExecutors(3)
    agent.setMode(Node.Mode.EXCLUSIVE)
    agent.setLabelString('tier-gold eu-west')
    j.addNode(agent)
    j.save()
    println \"CREATED_NODE: \${name}\"
} else {
    println \"EXISTS_NODE: \${name}\"
}
"
}

echo "=== 1. Idempotent Node Registration (Run #1 & Run #2) ==="
RUN1=$(register_node)
echo "Run #1: ${RUN1}"
RUN2=$(register_node)
echo "Run #2: ${RUN2}"
echo "${RUN2}" | grep -q "EXISTS_NODE: ${NODE_NAME}"

echo ""
echo "=== 2. REST Fleet Audit ==="
AUDIT_JSON=$(curl -s -f -g "${JENKINS_URL}/computer/${NODE_NAME}/api/json?tree=displayName,numExecutors,assignedLabels[name]")
echo "Audit JSON: ${AUDIT_JSON}"
echo "${AUDIT_JSON}" | grep -q "\"displayName\":\"${NODE_NAME}\""
echo "${AUDIT_JSON}" | grep -q "\"numExecutors\":3"
echo "${AUDIT_JSON}" | grep -q "tier-gold"
echo "${AUDIT_JSON}" | grep -q "eu-west"

echo ""
echo "=== 3. Idempotent Quarantine (Cordon) ==="
OFFLINE_STATE=$(curl -s -f -g "${JENKINS_URL}/computer/${NODE_NAME}/api/json?tree=temporarilyOffline,offlineCauseReason")
echo "Before cordon: ${OFFLINE_STATE}"

if echo "${OFFLINE_STATE}" | grep -q '"temporarilyOffline":false'; then
    curl -s -f -X POST "${JENKINS_URL}/computer/${NODE_NAME}/toggleOffline?offlineMessage=PT1%20Audit%20Lock" > /dev/null
fi

AFTER_CORDON=$(curl -s -f -g "${JENKINS_URL}/computer/${NODE_NAME}/api/json?tree=temporarilyOffline,offlineCauseReason")
echo "After cordon: ${AFTER_CORDON}"
echo "${AFTER_CORDON}" | grep -q '"temporarilyOffline":true'
echo "${AFTER_CORDON}" | grep -q "PT1 Audit Lock"

echo ""
echo "=== 4. Graceful Decommissioning ==="
REMOVED_OUT=$(curl -s -f -X POST "${JENKINS_URL}/scriptText" \
  --data-urlencode "script=
import jenkins.model.Jenkins

def j = Jenkins.get()
def node = j.getNode('${NODE_NAME}')
if (node == null) {
    println 'NODE_NOT_FOUND'
} else if (node.toComputer()?.isIdle()) {
    j.removeNode(node)
    j.save()
    println 'REMOVED_NODE: ${NODE_NAME}'
} else {
    println 'NODE_BUSY'
    System.exit(1)
}
")
echo "Decommission output: ${REMOVED_OUT}"
echo "${REMOVED_OUT}" | grep -q "REMOVED_NODE: ${NODE_NAME}"

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -g "${JENKINS_URL}/computer/${NODE_NAME}/api/json")
echo "HTTP status after removal: ${HTTP_STATUS}"
if [ "${HTTP_STATUS}" != "404" ]; then
    echo "[ERROR] Expected HTTP 404, got ${HTTP_STATUS}"
    exit 1
fi

echo ""
echo "[SUCCESS] Practice Test 1 passed completely!"
