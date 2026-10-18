#!/usr/bin/env bash
set -euo pipefail

echo "================================================================="
echo "Provisioning Jenkins Job: student-lab-resilience"
echo "================================================================="

# 1. Создаем Groovy-скрипт (тут работает Groovy-синтаксис для Jenkins)
cat << 'EOF' > script.groovy
import jenkins.model.*
import hudson.model.*
import hudson.tasks.Shell

def instance = Jenkins.get()
def jobName = 'student-lab-resilience'

// Получаем или создаем Freestyle Project
def job = instance.getItem(jobName) ?: instance.createProject(FreeStyleProject, jobName)

// А здесь внутри — чистый Bash-скрипт, который выполнится при сборке в Jenkins
def multiLineShell = '''#!/usr/bin/env bash
set -euo pipefail

# 2. Post-Execution Trap
cleanup() {
    echo "[CLEANUP] Removing temporary artifacts..."
    rm -f /tmp/student_build.tmp
}
trap cleanup EXIT

# 3. Artifact & File Generation
echo "--> Step 3: Generating temporary file and deployment JSON..."
touch /tmp/student_build.tmp

cat << 'JSON_EOF' > deployment.json
{
  "environment": "STAGING",
  "service": "api-gateway",
  "status": "HEALTHY"
}
JSON_EOF

echo "Generated deployment.json contents:"
cat deployment.json

# 4. Conditional Error Logic
SIMULATE_FAILURE="${SIMULATE_FAILURE:-FALSE}"

if [ "$SIMULATE_FAILURE" = "TRUE" ]; then
    echo "[ERROR] Simulated pipeline failure detected!" >&2
    exit 1
else
    echo "[SUCCESS] Deployment manifest generated."
    exit 0
fi
'''

job.getBuildersList().clear()
job.getBuildersList().add(new Shell(multiLineShell))
job.save()
instance.reload()

println "JOB_STUDENT_LAB_RESILIENCE_PROVISIONED"
EOF

# 2. Отправляем готовый Groovy-скрипт на Jenkins через Script Console
echo "--> Deploying job configuration via Jenkins Script Console..."
curl -s -X POST "http://localhost:8080/scriptText" \
  -u "admin:$API_TOKEN" \
  --data-urlencode "script@script.groovy"
rm script.groovy

# 3. Запускаем сборку для проверки
echo "--> Triggering build for student-lab-resilience..."
curl -X POST -s -u "admin:$API_TOKEN" "http://localhost:8080/job/student-lab-resilience/build"

echo "--> Waiting 5 seconds for execution..."
sleep 5

echo "=========================================================="
echo "--> BUILD CONSOLE OUTPUT:"
echo "=========================================================="
curl -s -u "admin:$API_TOKEN" "http://localhost:8080/job/student-lab-resilience/1/consoleText"
echo "=========================================================="