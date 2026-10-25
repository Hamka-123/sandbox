# 1. Запускаем локальный Jenkins в Docker с отключенным мастером установки и отключенной CSRF-защитой
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -e JAVA_OPTS="-Djenkins.install.runSetupWizard=false -Dhudson.security.csrf.GlobalCrumbIssuerConfiguration.DISABLE_CSRF_PROTECTION=true" \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts

echo "Waiting for Jenkins to initialize (15 seconds)..."
sleep 15

# 2. Создаем Groovy-скрипт внутри контейнера для настройки джобы с Shell-шагом и параметром
docker exec -i jenkins bash << 'EOF'
cd /tmp
cat << 'GROOVY_EOF' > script.groovy
import jenkins.model.*
import hudson.model.*
import hudson.tasks.Shell

def instance = Jenkins.get()
def jobName = 'lesson6-artifact-demo'

def job = instance.getItem(jobName) ?: instance.createProject(FreeStyleProject, jobName)

// Регистрируем строковый параметр окружения
def envParam = new StringParameterDefinition('BUILD_ENV', 'STAGING', 'Target Environment')
job.removeProperty(ParametersDefinitionProperty.class)
job.addProperty(new ParametersDefinitionProperty(envParam))

def shellScript = '''#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo "  HOURS 1-2: WORKSPACE ARTIFACT GENERATION"
echo "=========================================================="

echo "--> Step 1: Creating build workspace directories..."
mkdir -p ./output/reports

echo "--> Step 2: Generating build manifest artifact..."
cat << MANIFEST > ./output/build_manifest.json
{
  "job_name": "\${JOB_NAME}",
  "build_number": "\${BUILD_NUMBER}",
  "environment": "\${BUILD_ENV}",
  "timestamp": "\$(date -u +'%Y-%m-%dT%H:%M:%SZ')",
  "status": "SUCCESS"
}
MANIFEST

echo "--> Step 3: Generating execution log report..."
echo "[INFO] Build started for environment \${BUILD_ENV}" > ./output/reports/execution.log
echo "[INFO] Artifacts generated successfully at \$(date)" >> ./output/reports/execution.log

echo -e "\\n--> Step 4: Listing generated workspace files:"
ls -la ./output/
ls -la ./output/reports/
'''

job.getBuildersList().clear()
job.getBuildersList().add(new Shell(shellScript))
job.save()

println "LESSON6_HOURS1_2_PROVISIONED"
GROOVY_EOF

# 3. Отправляем Groovy-скрипт через REST API в Jenkins
curl -s -X POST "http://localhost:8080/scriptText" \
  --data-urlencode "script@script.groovy"
rm script.groovy
EOF

echo -e "\n=========================================================="
echo "3. Triggering build with BUILD_ENV=PRODUCTION..."
echo "=========================================================="

# 4. Запускаем сборку с параметром PRODUCTION через API
curl -X POST -s \
  "http://localhost:8080/job/lesson6-artifact-demo/buildWithParameters?BUILD_ENV=PRODUCTION"

echo "Waiting for build to complete..."
sleep 5

# 5. Выводим консольный лог последней сборки
echo -e "\n=========================================================="
echo "  CONSOLE LOG OUTPUT (LAST BUILD)"
echo "=========================================================="
curl -s "http://localhost:8080/job/lesson6-artifact-demo/lastBuild/consoleText"

# 6. Проверяем доступность манифеста артефактов через HTTP
echo -e "\n=========================================================="
echo "  FETCHING MANIFEST ARTIFACT OVER HTTP"
echo "=========================================================="
curl -s "http://localhost:8080/job/lesson6-artifact-demo/ws/output/build_manifest.json"
echo ""