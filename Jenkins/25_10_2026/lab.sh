# 1. Generate and deploy Capstone Provisioning Script
cat << 'EOF' > capstone_provision2.groovy
import jenkins.model.*
import hudson.model.*
import hudson.tasks.Shell

def instance = Jenkins.get()
def jobName = 'FreeStyleProject'

def job = instance.getItem(jobName) ?: instance.createProject(FreeStyleProject, jobName)

def paramApp = new StringParameterDefinition('MODULE_NAME', 'auth-module', 'Module Name')
def paramVer = new StringParameterDefinition('BUILD_NUMBER_ID', '101', 'Build number id')

job.removeProperty(ParametersDefinitionProperty.class)
job.addProperty(new ParametersDefinitionProperty(paramApp, paramVer))

def capstoneShell = '''#!/usr/bin/env bash
set -euo pipefail

teardown() {
    echo -e "\n[LAB-TEARDOWN] Workspace check completed."
}
trap teardown EXIT


echo "--> Step 1: Executing file validation gates..."
if [ ! -f "./some_required_file.txt" ]; then
    echo "[WARNING] Required file not found, marking build as FAILED."
    STATUS="FAILED"
fi

mkdir -p ./build_out

cat << MANIFEST > ./build_out/manifest.json
{
  "module": "<MODULE_NAME>",
  "build_id": "<BUILD_NUMBER_ID>",
  "status": $STATUS
}
MANIFEST

echo "--> Step 2: Executing file validation gates..."
if [ ! -s "./build_out/manifest.json" ]; then
    echo "[ERROR] Release manifest missing or empty!" >&2
    exit 1
fi

if [ "$status" != "PASS" ]; then
    echo "[ERROR] status: "PASS" is missing. " >&2
    exit 1
fi

echo "[SUCCESS] Release manifest integrity verified."

echo -e "\n--> Step 3: Manifest Artifact Contents:"
cat ./build_out/manifest.json
'''

job.getBuildersList().clear()
job.getBuildersList().add(new Shell(capstoneShell))
job.save()

println "LESSON6_CAPSTONE_PROVISIONED"
EOF

# 2. Deploy payload to Jenkins
curl -s -X POST "http://localhost:8080/scriptText" \
  -u "admin:$API_TOKEN" \
  --data-urlencode "script@capstone_provision2.groovy"
rm capstone_provision2.groovy


Bash (do step by step)

# 1. Query upcoming build ID
NEXT_BUILD_NUM=$(curl -s -u "admin:$API_TOKEN" \
  "http://localhost:8080/job/FreeStyleProject/api/json" \
  | grep -o '"nextBuildNumber":[^,]*' | cut -d':' -f2)

echo "--> Triggering Capstone Build #${NEXT_BUILD_NUM}..."

# 2. Trigger build with custom parameters
curl -X POST -s -u "admin:$API_TOKEN" \
  "http://localhost:8080/job/FreeStyleProject/buildWithParameters?BUILD_NUMBER_ID=${NEXT_BUILD_NUM}&"

echo "Waiting for build to finish..."
sleep 4

# 3. Stream console output for the build
echo "=========================================================="
echo "CONSOLE LOG (LAST BUILD)"
echo "=========================================================="
curl -s -u "admin:$API_TOKEN" "http://localhost:8080/job/FreeStyleProject/lastBuild/consoleText"

# 4. Fetch the generated artifact directly from the workspace via REST API
echo -e "\n=========================================================="
echo "  FETCHING ARTIFACT VIA WORKSPACE REST API (/ws/dist/release.json)"
echo "=========================================================="
curl -s -u "admin:$API_TOKEN" "http://localhost:8080/job/FreeStyleProject/ws/build_out/manifest.json"
echo ""