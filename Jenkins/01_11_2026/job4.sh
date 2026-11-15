#! /bin/bash 

cat << 'EOF' > script.groovy
import jenkins.model.*
import hudson.model.*
import hudson.tasks.Shell

def instance = Jenkins.get()
def jobName = 'lesson7-parallel-demo'
def job = instance.getItem(jobName)

String fallbackShellScript = '''#!/usr/bin/env bash
set -euo pipefail

mkdir -p ./build_out

echo "=========================================================="
echo "  HOURS 7-8: MULTI-STAGE FALLBACK GATES"
echo "=========================================================="

PRIMARY_REGION="us-east-1"
FAILOVER_REGION="us-west-2"

primary_deployment() {
    echo "--> Attempting deployment to Primary Region (${PRIMARY_REGION})..."
    # Simulate primary site failure
    return 1
}

secondary_fallback_deployment() {
    echo "--> [FALLBACK ACTIVATED] Deploying to Secondary Region (${FAILOVER_REGION})..."
    echo '{"active_site": "'"${FAILOVER_REGION}"'", "status": "FAILOVER_SUCCESS"}' > ./build_out/deployment.json
    echo "[FALLBACK SUCCESS] Secondary site online and routing traffic."
}

# Execute primary deployment step
PRIMARY_FAILED=0
set +e
primary_deployment
if [ $? -ne 0 ]; then
    PRIMARY_FAILED=1
fi
set -e

# Route execution based on primary status flag
if [ "${PRIMARY_FAILED}" -eq 1 ]; then
    echo "[WARNING] Primary region deployment failed!" >&2
    secondary_fallback_deployment
else
    echo '{"active_site": "'"${PRIMARY_REGION}"'", "status": "PRIMARY_SUCCESS"}' > ./build_out/deployment.json
    echo "[SUCCESS] Primary region deployment completed."
fi

echo -e "\n--> Final Deployment State Manifest:"
cat ./build_out/deployment.json
'''

job.getBuildersList().clear()
job.getBuildersList().add(new Shell(fallbackShellScript))
job.save()

println "LESSON7_HOURS7_8_PROVISIONED"
EOF

curl -s -X POST "http://localhost:8080/scriptText" \
  -u "admin:$API_TOKEN" \
  --data-urlencode "script@script.groovy"
rm script.groovy



NEXT_BUILD_NUM=$(curl -s -u "admin:$API_TOKEN" \
  "http://localhost:8080/job/lesson7-parallel-demo/api/json" \
  | sed -n 's/.*"nextBuildNumber":\([0-9]*\).*/\1/p')

if [ -z "${NEXT_BUILD_NUM}" ]; then
  NEXT_BUILD_NUM=1
fi

curl -X POST -s -u "admin:$API_TOKEN" "http://localhost:8080/job/lesson7-parallel-demo/buildWithParameters"

sleep 4

curl -s -u "admin:$API_TOKEN" "http://localhost:8080/job/lesson7-parallel-demo/${NEXT_BUILD_NUM}/consoleText"

# Started by user unknown or anonymous
# Running as SYSTEM
# Building in workspace /var/jenkins_home/workspace/lesson7-parallel-demo
# [lesson7-parallel-demo] $ /usr/bin/env bash /tmp/jenkins413987503153832176.sh
# ==========================================================
#   HOURS 7-8: MULTI-STAGE FALLBACK GATES
# ==========================================================
# --> Attempting deployment to Primary Region (us-east-1)...
# [WARNING] Primary region deployment failed!
# --> [FALLBACK ACTIVATED] Deploying to Secondary Region (us-west-2)...
# [FALLBACK SUCCESS] Secondary site online and routing traffic.

# --> Final Deployment State Manifest:
# {"active_site": "us-west-2", "status": "FAILOVER_SUCCESS"}
# Finished: SUCCESS

