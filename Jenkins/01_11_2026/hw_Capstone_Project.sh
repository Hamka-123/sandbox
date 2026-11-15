#! /bin/bash

cat << 'EOF' > script.groovy
import jenkins.model.*
import hudson.model.*
import hudson.tasks.Shell

def instance = Jenkins.get()
def jobName = 'lesson7-capstone-pipeline'
def job = instance.getItem(jobName) ?: instance.createProject(FreeStyleProject, jobName)

// Регистрация параметров сборки
def p1 = new StringParameterDefinition('SERVICE_COUNT', '3', 'Number of service workers')
def p2 = new StringParameterDefinition('SIMULATE_FAILURE', 'false', 'Simulate worker failure')
job.removeProperty(ParametersDefinitionProperty.class)
job.addProperty(new ParametersDefinitionProperty([p1, p2]))

String capstoneScript = '''#!/usr/bin/env bash
set -euo pipefail

mkdir -p ./build_out ./logs

ACTIVE_PIDS=()

# Очистка зависших процессов при выходе
cleanup() {
    local exit_code=$?
    echo "[CLEANUP] Terminating active background processes..."
    for pid in "${ACTIVE_PIDS[@]}"; do
        if kill -0 "${pid}" 2>/dev/null; then
            kill -9 "${pid}" 2>/dev/null || true
        fi
    done
}
trap cleanup EXIT SIGTERM

echo "=========================================================="
echo "  CAPSTONE: SELF-HEALING PARALLEL PROCESSING ENGINE"
echo "=========================================================="

FAILED=0

worker_task() {
    local id=$1
    local simulate_fail=$2
    local attempt=1
    local max_attempts=3

    while [ "${attempt}" -le "${max_attempts}" ]; do
        echo "[WORKER ${id}] Attempt ${attempt}/${max_attempts}..."
        if [ "${simulate_fail}" = "true" ] && [ "${id}" -eq 2 ]; then
            echo "[WORKER ${id}] Simulated failure on worker 2" >&2
            return 1
        fi
        sleep 1
        return 0
    done
    return 1
}

# Запуск воркеров в фоновом режиме
for ((i=1; i<=SERVICE_COUNT; i++)); do
    (
        worker_task "${i}" "${SIMULATE_FAILURE}" || exit 1
    ) &
    PID=$!
    ACTIVE_PIDS+=("${PID}")
    echo "[SPAWNED] Worker ${i} with PID ${PID}"
done

# Watchdog таймер (лимит 5 секунд)
(
    sleep 5
    for pid in "${ACTIVE_PIDS[@]}"; do
        if kill -0 "${pid}" 2>/dev/null; then
            echo "[TIMEOUT] Watchdog killing hanging PID ${pid}" >&2
            kill -15 "${pid}" 2>/dev/null || true
        fi
    done
) &
WATCHDOG_PID=$!
ACTIVE_PIDS+=("${WATCHDOG_PID}")

# Синхронизация и ожидание воркеров
for pid in "${ACTIVE_PIDS[@]}"; do
    if [ "${pid}" = "${WATCHDOG_PID}" ]; then continue; fi
    if ! wait "${pid}"; then
        FAILED=1
    fi
done

# Роутинг при сбое или успехе
if [ "${FAILED}" -ne 0 ]; then
    echo "[EMERGENCY] Pipeline failure detected. Writing emergency manifest..." >&2
    echo '{"status": "EMERGENCY_FAILOVER", "error": "Worker execution failed or timed out"}' > ./build_out/emergency.json
    exit 1
else
    echo '{"status": "SUCCESS", "message": "All services synchronized successfully"}' > ./build_out/emergency.json
    echo "[SUCCESS] Pipeline completed cleanly."
fi
'''

job.getBuildersList().clear()
job.getBuildersList().add(new Shell(capstoneScript))
job.save()

println "CAPSTONE_PROVISIONED"
EOF

# Деплой в Jenkins
curl -s -X POST "http://localhost:8080/scriptText" \
  -u "admin:$API_TOKEN" \
  --data-urlencode "script@script.groovy"
rm script.groovy

# Запуск и вывод логов
NEXT_BUILD_NUM=$(curl -s -u "admin:$API_TOKEN" \
  "http://localhost:8080/job/lesson7-capstone-pipeline/api/json" \
  | sed -n 's/.*"nextBuildNumber":\([0-9]*\).*/\1/p')

[ -z "${NEXT_BUILD_NUM}" ] && NEXT_BUILD_NUM=1

curl -X POST -s -u "admin:$API_TOKEN" \
  "http://localhost:8080/job/lesson7-capstone-pipeline/buildWithParameters?SIMULATE_FAILURE=true"

sleep 6

curl -s -u "admin:$API_TOKEN" "http://localhost:8080/job/lesson7-capstone-pipeline/${NEXT_BUILD_NUM}/consoleText"


# Started by user unknown or anonymous
# Running as SYSTEM
# Building in workspace /var/jenkins_home/workspace/lesson7-capstone-pipeline
# [lesson7-capstone-pipeline] $ /usr/bin/env bash /tmp/jenkins14951889536242898710.sh
# ==========================================================
#   CAPSTONE: SELF-HEALING PARALLEL PROCESSING ENGINE
# ==========================================================
# [SPAWNED] Worker 1 with PID 1678
# [WORKER 1] Attempt 1/3...
# [SPAWNED] Worker 2 with PID 1679
# [WORKER 2] Attempt 1/3...
# [SPAWNED] Worker 3 with PID 1680
# [WORKER 2] Simulated failure on worker 2
# [WORKER 3] Attempt 1/3...
# [EMERGENCY] Pipeline failure detected. Writing emergency manifest...
# [CLEANUP] Terminating active background processes...
# Build step 'Execute shell' marked build as failure
# Finished: FAILURE
# jenkins@6491cff57655:/tmp$ 

# проверить содержимое файла emergency.json через REST API Jenkins
curl -s -u "admin:$API_TOKEN" \
  "http://localhost:8080/job/lesson7-capstone-pipeline/ws/build_out/emergency.json"