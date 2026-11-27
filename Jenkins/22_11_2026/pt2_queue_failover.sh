#!/usr/bin/env bash
set -euo pipefail

JENKINS_URL="http://localhost:8080"
AGENT_NAME="pt2-offline-agent"
JOB_NAME="pt2-failover-job"

echo "=== 1. Self-Contained Setup ==="
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

// 1. Register virtual agent bound to isolated-zone
def existingNode = j.getNode('${AGENT_NAME}')
if (existingNode == null) {
    def agent = new DumbSlave(
        '${AGENT_NAME}',
        '/tmp/jenkins-agent-pt2',
        new JNLPLauncher(true)
    )
    agent.setNumExecutors(1)
    agent.setMode(Node.Mode.EXCLUSIVE)
    agent.setLabelString('isolated-zone')
    j.addNode(agent)
    println 'CREATED_AGENT: ${AGENT_NAME}'
} else {
    existingNode.setLabelString('isolated-zone')
    existingNode.setMode(Node.Mode.EXCLUSIVE)
    println 'UPDATED_AGENT: ${AGENT_NAME}'
}

// 2. Create or update Freestyle job bound to isolated-zone
def job = j.getItem('${JOB_NAME}') ?: j.createProject(FreeStyleProject, '${JOB_NAME}')
job.setAssignedLabel(j.getLabel('isolated-zone'))

def cmd = '''#!/usr/bin/env bash
set -euo pipefail
TARGET_NODE=\"\${NODE_NAME:-built-in}\"
echo \"RAN_ON=\${TARGET_NODE}\" > where.txt
cat where.txt
'''

job.getBuildersList().clear()
job.getBuildersList().add(new Shell(cmd))

job.getPublishersList().clear()
def archiver = new ArtifactArchiver('where.txt')
archiver.setOnlyIfSuccessful(true)
job.getPublishersList().add(archiver)

job.save()
j.save()
println 'SETUP_COMPLETE: ${JOB_NAME} -> isolated-zone'
"

# Ensure pt2-offline-agent is offline so the queued item stalls
IS_OFFLINE=$(curl -s -f -g "${JENKINS_URL}/computer/${AGENT_NAME}/api/json?tree=temporarilyOffline" \
  | sed -n 's/.*"temporarilyOffline":\([a-z]*\).*/\1/p')
if [ "${IS_OFFLINE}" != "true" ]; then
    curl -s -f -X POST "${JENKINS_URL}/computer/${AGENT_NAME}/toggleOffline?offlineMessage=PT2%20Simulated%20Offline" > /dev/null
fi
echo "Agent ${AGENT_NAME} offline state verified."

echo ""
echo "=== 2. Trigger & Stall Verification ==="
HEADERS=$(curl -s -f -D - -o /dev/null -X POST "${JENKINS_URL}/job/${JOB_NAME}/build?delay=0sec")
QUEUE_URL=$(echo "${HEADERS}" | grep -i "^Location:" | head -n 1 | cut -d' ' -f2- | tr -d '\r\n ' )
echo "Queue URL: [${QUEUE_URL}]"
if [ -z "${QUEUE_URL}" ]; then
    echo "[ERROR] Failed to capture Location header"
    exit 1
fi

sleep 2
QUEUE_INFO=$(curl -s -f -g "${QUEUE_URL}api/json?tree=id,why")
echo "Queue info while stalled: ${QUEUE_INFO}"
echo "${QUEUE_INFO}" | grep -qi "offline"

echo ""
echo "=== 3. Live Label Failover ==="
curl -s -f -X POST "${JENKINS_URL}/scriptText" \
  --data-urlencode "script=
import jenkins.model.Jenkins

def j = Jenkins.get()
def job = j.getItem('${JOB_NAME}')
if (job == null) {
    throw new IllegalStateException('Job not found: ${JOB_NAME}')
}
job.setAssignedLabel(j.getLabel('built-in'))
job.save()
println 'REBOUND_JOB: ${JOB_NAME} -> built-in'
"

echo ""
echo "=== 4. Drain & Placement Proof ==="
BUILD_NUM=""
while [ -z "${BUILD_NUM}" ]; do
    sleep 1
    Q_JSON=$(curl -s -g "${QUEUE_URL}api/json?tree=executable[number],cancelled" || true)
    if echo "${Q_JSON}" | grep -q '"cancelled":true'; then
        echo "[ERROR] Queue item was cancelled"
        exit 1
    fi
    BUILD_NUM=$(echo "${Q_JSON}" | sed -n 's/.*"number":\([0-9]*\).*/\1/p')
done
echo "Resolved build number: #${BUILD_NUM}"

while true; do
    B_JSON=$(curl -s -f -g "${JENKINS_URL}/job/${JOB_NAME}/${BUILD_NUM}/api/json?tree=building,result")
    BUILDING=$(echo "${B_JSON}" | sed -n 's/.*"building":\([a-z]*\).*/\1/p')
    if [ "${BUILDING}" = "false" ]; then
        RESULT=$(echo "${B_JSON}" | sed -n 's/.*"result":"\([^"]*\)".*/\1/p')
        break
    fi
    sleep 1
done

echo "Build #${BUILD_NUM} finished with result: ${RESULT}"
if [ "${RESULT}" != "SUCCESS" ]; then
    echo "[ERROR] Expected SUCCESS, got ${RESULT}"
    exit 1
fi

curl -s -f -o "where.txt" "${JENKINS_URL}/job/${JOB_NAME}/${BUILD_NUM}/artifact/where.txt"
ARTIFACT_CONTENT=$(cat where.txt | tr -d '\r')
echo "Downloaded where.txt: [${ARTIFACT_CONTENT}]"
echo "${ARTIFACT_CONTENT}" | grep -q "RAN_ON=built-in"

echo ""
echo "=== 5. Cleanup ==="
curl -s -f -X POST "${JENKINS_URL}/scriptText" \
  --data-urlencode "script=
import jenkins.model.Jenkins

def j = Jenkins.get()
def node = j.getNode('${AGENT_NAME}')
if (node != null && node.toComputer()?.isIdle()) {
    j.removeNode(node)
    j.save()
    println 'CLEANED_AGENT: ${AGENT_NAME}'
}
"

echo ""
echo "[SUCCESS] Practice Test 2 passed completely!"
