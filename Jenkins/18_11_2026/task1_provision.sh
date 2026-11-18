#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -euo pipefail

# Define Jenkins base URL
JENKINS_URL="${JENKINS_URL:-http://localhost:8080}"

# Define the Groovy script payload to provision the Freestyle job idempotently
read -r -d '' GROOVY_SCRIPT << 'EOF' || true
import jenkins.model.Jenkins
import hudson.model.FreeStyleProject
import hudson.model.StringParameterDefinition
import hudson.model.BooleanParameterDefinition
import hudson.model.ParametersDefinitionProperty
import hudson.tasks.Shell
import hudson.tasks.ArtifactArchiver

def jobName = "lab-provision-check"
def jenkins = Jenkins.get()
def job = jenkins.getItem(jobName)

// Check if job exists, create or update in place
if (job == null) {
    println "Creating new job: ${jobName}"
    job = jenkins.createProject(FreeStyleProject.class, jobName)
} else {
    println "Job ${jobName} already exists. Updating in place."
}

// Configure parameters (APP_VERSION and DRY_RUN)
def paramDefProp = new ParametersDefinitionProperty(
    new StringParameterDefinition("APP_VERSION", "1.0.0", "Application version"),
    new BooleanParameterDefinition("DRY_RUN", false, "Dry run flag")
)
job.removeProperty(ParametersDefinitionProperty.class)
job.addProperty(paramDefProp)

// Configure Shell build step
job.getBuildersList().clear()
def shellBuilder = new Shell('''rm -f manifest.txt
echo "version=\${APP_VERSION}" >> manifest.txt
echo "dry_run=\${DRY_RUN}" >> manifest.txt''')
job.getBuildersList().add(shellBuilder)

// Configure Post-build action (ArtifactArchiver) for manifest.txt with onlyIfSuccessful = true
job.getPublishersList().clear()
def archiver = new ArtifactArchiver("manifest.txt")
archiver.setOnlyIfSuccessful(true)
job.getPublishersList().add(archiver)

// Save the job configuration and print confirmation
job.save()
println "Job ${jobName} successfully provisioned and saved."
EOF

echo "=== Run 1: Initial Provisioning ==="
curl -s -X POST "${JENKINS_URL}/scriptText" \
  --data-urlencode "script=${GROOVY_SCRIPT}"
echo ""

echo "=== Run 2: Idempotency Proof (Re-running provisioning logic) ==="
curl -s -X POST "${JENKINS_URL}/scriptText" \
  --data-urlencode "script=${GROOVY_SCRIPT}"
echo ""

echo "=== Verification via REST API (Exact Tree Query) ==="
API_URL="${JENKINS_URL}/job/lab-provision-check/api/json?tree=name,property[parameterDefinitions[name,defaultParameterValue[value]]]"
RESPONSE=$(curl -sS -g "${API_URL}")

echo "Raw JSON response:"
echo "${RESPONSE}"
echo ""

echo "Parsed Parameter Summary:"
echo "${RESPONSE}" \
  | grep -o '"name":"[^"]*"\|"value":[^,}]*' \
  | sed 's/"name":"//; s/"$//; s/"value":/ = /' \
  | awk '
      !/^ = / && $0 == "lab-provision-check" { next }
      !/^ = / { param = $0 }
      /^ = /  {
        sub(/^ = /, "", $0)
        print "  - Parameter: " param " (default value: " $0 ")"
      }
    '
echo ""

echo "=== Triggering Parameterized Build ==="
curl -s -X POST "${JENKINS_URL}/job/lab-provision-check/buildWithParameters" \
  --data-urlencode "APP_VERSION=1.0.0" \
  --data-urlencode "DRY_RUN=false"
echo "Build triggered. Waiting for build completion..."

# Polling loop: check Jenkins build status until it finishes
BUILD_STATUS=""
for i in {1..30}; do
    sleep 1
    # Check if a successful build or any finished build exists
    BUILD_RESULT=$(curl -s -g "${JENKINS_URL}/job/lab-provision-check/lastBuild/api/json?tree=result" | grep -o '"result":"[^"]*"' | cut -d'"' -f4 || true)
    if [ "${BUILD_RESULT}" = "SUCCESS" ]; then
        echo "Build completed successfully!"
        break
    elif [ "${BUILD_RESULT}" = "FAILURE" ] || [ "${BUILD_RESULT}" = "ABORTED" ]; then
        echo "Build finished with status: ${BUILD_RESULT}"
        exit 1
    fi
    echo -n "."
done
echo ""

echo "=== Downloading and Verifying manifest.txt Artifact ==="
if curl -sS -O "${JENKINS_URL}/job/lab-provision-check/lastSuccessfulBuild/artifact/manifest.txt"; then
    echo "Successfully downloaded manifest.txt:"
    echo "----------------------------------------"
    cat manifest.txt
    echo "----------------------------------------"
    rm -f manifest.txt
else
    echo "Failed to download manifest.txt. Make sure the build completed successfully."
fi