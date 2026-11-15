#! /bin/bash

cat << 'EOF' > script.groovy
import jenkins.model.*
import hudson.model.*
import hudson.tasks.Shell

def instance = Jenkins.get()
def jobName = 'lesson7-parallel-demo'
def job = instance.getItem(jobName)

String timeoutShellScript = '''#!/usr/bin/env bash
set -euo pipefail

# Maximum allowable execution window in seconds
TIMEOUT_LIMIT=3

echo "=========================================================="
echo "  HOURS 3-4: PROCESS ISOLATION & TIMEOUT GUARDS"
echo "=========================================================="

# Global PID cleanup registry
ACTIVE_PIDS=()

# Comprehensive termination handler to kill orphaned processes
cleanup_processes() {
    local exit_code=$?
    echo -e "\n[CLEANUP] Executing process isolation sweep (Exit Code: ${exit_code})..."
    for pid in "${ACTIVE_PIDS[@]}"; do
        if kill -0 "${pid}" 2>/dev/null; then
            echo "  [TERMINATING] Terminating lingering process PID ${pid}..."
            kill -9 "${pid}" 2>/dev/null || true
        fi
    done
}

# Bind cleanup handler to EXIT and SIGTERM signals
trap cleanup_processes EXIT SIGTERM

# Simulate long-running worker subshell
long_running_worker() {
    echo "[WORKER] Initialized hanging work thread (PID $$)..."
    # Intentionally exceeds the 3-second limit
    sleep 10
    echo "[WORKER] Task finished successfully."
}

# 1. Launch worker in background
long_running_worker &
WORKER_PID=$!
ACTIVE_PIDS+=("${WORKER_PID}")
echo "--> Worker spawned with PID: ${WORKER_PID}"

# 2. Launch watchdog process in background
watchdog() {
    local target_pid=$1
    local limit=$2
    sleep "${limit}"
    if kill -0 "${target_pid}" 2>/dev/null; then
        echo -e "\n[TIMEOUT EXCEEDED] Worker PID ${target_pid} passed ${limit}s threshold!" >&2
        echo "[TIMEOUT EXCEEDED] Dispatching SIGTERM to force worker termination..." >&2
        kill -15 "${target_pid}" 2>/dev/null || true
    fi
}

watchdog "${WORKER_PID}" "${TIMEOUT_LIMIT}" &
WATCHDOG_PID=$!
ACTIVE_PIDS+=("${WATCHDOG_PID}")
echo "--> Watchdog initialized with PID: ${WATCHDOG_PID} (Limit: ${TIMEOUT_LIMIT}s)"

# 3. Wait for worker process
echo "--> Main process entering synchronization block..."
if wait "${WORKER_PID}"; then
    echo "[SUCCESS] Worker completed before timeout threshold."
    # Kill watchdog since worker completed naturally
    kill -9 "${WATCHDOG_PID}" 2>/dev/null || true
else
    echo "[FAILURE] Worker execution interrupted or terminated by watchdog!" >&2
    exit 1
fi
'''

job.getBuildersList().clear()
job.getBuildersList().add(new Shell(timeoutShellScript))
job.save()

println "LESSON7_HOURS3_4_PROVISIONED"
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

# Wait for watchdog to trigger (3-second timeout limit + queue buffers)
sleep 6

curl -s -u "admin:$API_TOKEN" "http://localhost:8080/job/lesson7-parallel-demo/${NEXT_BUILD_NUM}/consoleText"



# ==========================================================
#   HOURS 3-4: PROCESS ISOLATION & TIMEOUT GUARDS
# ==========================================================
# --> Worker spawned with PID: 1601
# [WORKER] Initialized hanging work thread (PID 1597)...
# --> Watchdog initialized with PID: 1603 (Limit: 3s)
# --> Main process entering synchronization block...



# Started by user unknown or anonymous
# Running as SYSTEM
# Building in workspace /var/jenkins_home/workspace/lesson7-parallel-demo
# [lesson7-parallel-demo] $ /usr/bin/env bash /tmp/jenkins678683877632325055.sh
# ==========================================================
#   HOURS 3-4: PROCESS ISOLATION & TIMEOUT GUARDS
# ==========================================================
# --> Worker spawned with PID: 1601
# [WORKER] Initialized hanging work thread (PID 1597)...
# --> Watchdog initialized with PID: 1603 (Limit: 3s)
# --> Main process entering synchronization block...

# [TIMEOUT EXCEEDED] Worker PID 1601 passed 3s threshold!
# [TIMEOUT EXCEEDED] Dispatching SIGTERM to force worker termination...
# [FAILURE] Worker execution interrupted or terminated by watchdog!

# [CLEANUP] Executing process isolation sweep (Exit Code: 1)...





# Started by user unknown or anonymous
# Running as SYSTEM
# Building in workspace /var/jenkins_home/workspace/lesson7-parallel-demo
# [lesson7-parallel-demo] $ /usr/bin/env bash /tmp/jenkins678683877632325055.sh
# ==========================================================
#   HOURS 3-4: PROCESS ISOLATION & TIMEOUT GUARDS
# ==========================================================
# --> Worker spawned with PID: 1601
# [WORKER] Initialized hanging work thread (PID 1597)...
# --> Watchdog initialized with PID: 1603 (Limit: 3s)
# --> Main process entering synchronization block...

# [TIMEOUT EXCEEDED] Worker PID 1601 passed 3s threshold!
# [TIMEOUT EXCEEDED] Dispatching SIGTERM to force worker termination...
# [FAILURE] Worker execution interrupted or terminated by watchdog!

# [CLEANUP] Executing process isolation sweep (Exit Code: 1)...
# Build step 'Execute shell' marked build as failure
# Finished: FAILURE