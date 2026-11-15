#! /bin/bash

cat << 'EOF' > script.groovy
import jenkins.model.*
import hudson.model.*
import hudson.tasks.Shell

def instance = Jenkins.get()
def jobName = 'lesson7-audit-aggregator'
def job = instance.getItem(jobName) ?: instance.createProject(FreeStyleProject, jobName)

// Регистрация параметров сборки
def p1 = new StringParameterDefinition('WORKER_COUNT', '4', 'Number of audit workers')
def p2 = new StringParameterDefinition('SIMULATE_LATENCY', 'true', 'Simulate work latency')
job.removeProperty(ParametersDefinitionProperty.class)
job.addProperty(new ParametersDefinitionProperty([p1, p2]))

String auditScript = '''#!/usr/bin/env bash
set -euo pipefail

mkdir -p ./logs ./build_out
ACTIVE_PIDS=()

cleanup() {
    local exit_code=$?
    for pid in "${ACTIVE_PIDS[@]}"; do
        if kill -0 "${pid}" 2>/dev/null; then
            kill -9 "${pid}" 2>/dev/null || true
        fi
    done
}
trap cleanup EXIT SIGTERM

echo "=========================================================="
echo "  EXTENSION: MULTITHREADED LOG AGGREGATOR & AUDIT"
echo "=========================================================="

worker_audit() {
    local id=$1
    local latency=$2
    local log_file="./logs/worker_${id}.log"
    local json_file="./logs/worker_${id}.json"

    echo "[WORKER ${id}] Starting audit task..." > "${log_file}"
    
    if [ "${latency}" = "true" ]; then
        local sleep_time=$(( (RANDOM % 3) + 1 ))
        sleep "${sleep_time}"
    fi

    echo "[WORKER ${id}] Completed successfully." >> "${log_file}"

    # Генерация JSON-отчета воркера
    cat << JSON > "${json_file}"
{
  "worker_id": "${id}",
  "pid": "\$\$",
  "status": "COMPLETED"
}
JSON
}

# Запуск параллельных воркеров
for ((i=1; i<=WORKER_COUNT; i++)); do
    worker_audit "${i}" "${SIMULATE_LATENCY}" &
    PID=$!
    ACTIVE_PIDS+=("${PID}")
    echo "  [SPAWNED] Audit Worker ${i} with PID ${PID}"
done

# Синхронизация потоков
FAILED=0
for pid in "${ACTIVE_PIDS[@]}"; do
    if ! wait "${pid}"; then
        echo "  [SYNC FAILURE] Process ${pid} failed." >&2
        FAILED=1
    fi
done

if [ "${FAILED}" -ne 0 ]; then
    echo "[ERROR] One or more audit workers failed!" >&2
    exit 1
fi

echo "--> Aggregating JSON payloads..."
echo "[" > ./build_out/audit_summary.json
first=true
for json in ./logs/worker_*.json; do
    if [ "$first" = true ]; then
        first=false
    else
        echo "," >> ./build_out/audit_summary.json
    fi
    cat "${json}" >> ./build_out/audit_summary.json
done
echo "]" >> ./build_out/audit_summary.json

echo "--> Generating MD5 Checksum..."
md5sum ./build_out/audit_summary.json | awk '{print $1}' > ./build_out/audit_summary.json.md5

echo "=========================================================="
echo "  AGGREGATED MANIFEST:"
cat ./build_out/audit_summary.json
echo -e "\n  MD5 CHECKSUM:"
cat ./build_out/audit_summary.json.md5
echo "=========================================================="
'''

job.getBuildersList().clear()
job.getBuildersList().add(new Shell(auditScript))
job.save()

println "AUDIT_AGGREGATOR_PROVISIONED"
EOF

# Деплой в Jenkins
curl -s -X POST "http://localhost:8080/scriptText" \
  -u "admin:$API_TOKEN" \
  --data-urlencode "script@script.groovy"
rm script.groovy

# Запуск и вывод логов
NEXT_BUILD_NUM=$(curl -s -u "admin:$API_TOKEN" \
  "http://localhost:8080/job/lesson7-audit-aggregator/api/json" \
  | sed -n 's/.*"nextBuildNumber":\([0-9]*\).*/\1/p')

[ -z "${NEXT_BUILD_NUM}" ] && NEXT_BUILD_NUM=1

curl -X POST -s -u "admin:$API_TOKEN" \
  "http://localhost:8080/job/lesson7-audit-aggregator/buildWithParameters"

sleep 5

curl -s -u "admin:$API_TOKEN" "http://localhost:8080/job/lesson7-audit-aggregator/${NEXT_BUILD_NUM}/consoleText"


# Started by user unknown or anonymous
# Running as SYSTEM
# Building in workspace /var/jenkins_home/workspace/lesson7-audit-aggregator
# [lesson7-audit-aggregator] $ /usr/bin/env bash /tmp/jenkins8724940108580175606.sh
# ==========================================================
#   EXTENSION: MULTITHREADED LOG AGGREGATOR & AUDIT
# ==========================================================
#   [SPAWNED] Audit Worker 1 with PID 1704
#   [SPAWNED] Audit Worker 2 with PID 1705
#   [SPAWNED] Audit Worker 3 with PID 1707
#   [SPAWNED] Audit Worker 4 with PID 1709
# --> Aggregating JSON payloads...
# --> Generating MD5 Checksum...
# ==========================================================
#   AGGREGATED MANIFEST:
# [
# {
#   "worker_id": "1",
#   "pid": "1699",
#   "status": "COMPLETED"
# }
# ,
# {
#   "worker_id": "2",
#   "pid": "1699",
#   "status": "COMPLETED"
# }
# ,
# {
#   "worker_id": "3",
#   "pid": "1699",
#   "status": "COMPLETED"
# }
# ,
# {
#   "worker_id": "4",
#   "pid": "1699",
#   "status": "COMPLETED"
# }
# ]

#   MD5 CHECKSUM:
# 7e0f104e8fe847e1951be8658a82acac
# ==========================================================
# Finished: SUCCESS