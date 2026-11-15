#! /bin/bash

cat << 'EOF' > script.groovy
import jenkins.model.*
import hudson.model.*
import hudson.tasks.Shell

def instance = Jenkins.get()
def jobName = 'lesson7-parallel-demo'

def job = instance.getItem(jobName) ?: instance.createProject(FreeStyleProject, jobName)

// Register parallel execution thread count parameter
def threadsParam = new StringParameterDefinition('PARALLEL_THREADS', '3', 'Number of parallel worker subshells')
job.removeProperty(ParametersDefinitionProperty.class)
job.addProperty(new ParametersDefinitionProperty(threadsParam))

String parallelShellScript = '''#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo "  HOURS 1-2: ASYNCHRONOUS SUBSHELL PARALLELISM"
echo "=========================================================="

# Directory for subshell thread logs
mkdir -p ./logs/threads

# Arrays to capture Process IDs (PIDs) and worker indices
PIDS=()
WORKERS=(${PARALLEL_THREADS})

echo "--> Step 1: Spawning ${PARALLEL_THREADS} parallel subshell tasks..."

worker_task() {
    local worker_id=$1
    local log_file="./logs/threads/worker_${worker_id}.log"
    
    echo "[WORKER ${worker_id}] Task started at $(date +%H:%M:%S)" > "${log_file}"
    
    # Simulate non-blocking asynchronous work with varying execution times
    local sleep_time=$(( (RANDOM % 3) + 1 ))
    sleep "${sleep_time}"
    
    echo "[WORKER ${worker_id}] Completed work in ${sleep_time}s" >> "${log_file}"
}

# Loop to spawn background subshells
for i in $(seq 1 "${PARALLEL_THREADS}"); do
    worker_task "${i}" &
    PID=$!
    PIDS+=("${PID}")
    echo "  [SPAWNED] Worker Thread ${i} assigned PID ${PID}"
done

echo -e "\n--> Step 2: Synchronizing subshell completion (Waiting on PIDs: ${PIDS[*]})..."

# Track failure states across threads
FAILED=0

for idx in "${!PIDS[@]}"; do
    PID="${PIDS[$idx]}"
    WORKER_NUM=$((idx + 1))
    
    if wait "${PID}"; then
        echo "  [SYNC SUCCESS] Worker ${WORKER_NUM} (PID ${PID}) finished cleanly."
    else
        echo "  [SYNC FAILURE] Worker ${WORKER_NUM} (PID ${PID}) exited with non-zero status!" >&2
        FAILED=1
    fi
done

if [ "${FAILED}" -ne 0 ]; then
    echo "[ERROR] One or more parallel subshells failed execution!" >&2
    exit 1
fi

echo -e "\n--> Step 3: Inspecting aggregated parallel thread logs:"
for log in ./logs/threads/*.log; do
    echo "--- File: ${log} ---"
    cat "${log}"
done

echo "[SUCCESS] All parallel tasks synchronized successfully."
'''

job.getBuildersList().clear()
job.getBuildersList().add(new Shell(parallelShellScript))
job.save()

println "LESSON7_HOURS1_2_PROVISIONED"
EOF

# Deploy to Jenkins via /scriptText
curl -s -X POST "http://localhost:8080/scriptText" \
  -u "admin:$API_TOKEN" \
  --data-urlencode "script@script.groovy"
rm script.groovy




# 1. Fetch upcoming build ID dynamically
NEXT_BUILD_NUM=$(curl -s -u "admin:$API_TOKEN" \
  "http://localhost:8080/job/lesson7-parallel-demo/api/json" \
  | sed -n 's/.*"nextBuildNumber":\([0-9]*\).*/\1/p')

if [ -z "${NEXT_BUILD_NUM}" ]; then
  NEXT_BUILD_NUM=1
fi

echo "--> Target Build Number: ${NEXT_BUILD_NUM}"

# 2. Trigger build with PARALLEL_THREADS=4
curl -X POST -s -u "admin:$API_TOKEN" \
  "http://localhost:8080/job/lesson7-parallel-demo/buildWithParameters?PARALLEL_THREADS=4"

# Wait for queue ingestion and parallel subshell execution
sleep 5

# 3. Stream console output
echo "=========================================================="
echo "  CONSOLE LOG OUTPUT (BUILD #${NEXT_BUILD_NUM})"
echo "=========================================================="
curl -s -u "admin:$API_TOKEN" "http://localhost:8080/job/lesson7-parallel-demo/${NEXT_BUILD_NUM}/consoleText"


#   CONSOLE LOG OUTPUT (BUILD #1)
# ==========================================================
# Started by user unknown or anonymous
# Running as SYSTEM
# Building in workspace /var/jenkins_home/workspace/lesson7-parallel-demo
# [lesson7-parallel-demo] $ /usr/bin/env bash /tmp/jenkins16502422470214167065.sh
# ==========================================================
#   HOURS 1-2: ASYNCHRONOUS SUBSHELL PARALLELISM
# ==========================================================
# --> Step 1: Spawning 4 parallel subshell tasks...
#   [SPAWNED] Worker Thread 1 assigned PID 1541
#   [SPAWNED] Worker Thread 2 assigned PID 1543
#   [SPAWNED] Worker Thread 3 assigned PID 1545
#   [SPAWNED] Worker Thread 4 assigned PID 1547

# --> Step 2: Synchronizing subshell completion (Waiting on PIDs: 1541 1543 1545 1547)...
#   [SYNC SUCCESS] Worker 1 (PID 1541) finished cleanly.
#   [SYNC SUCCESS] Worker 2 (PID 1543) finished cleanly.
#   [SYNC SUCCESS] Worker 3 (PID 1545) finished cleanly.
#   [SYNC SUCCESS] Worker 4 (PID 1547) finished cleanly.

# --> Step 3: Inspecting aggregated parallel thread logs:
# --- File: ./logs/threads/worker_1.log ---
# [WORKER 1] Task started at 18:29:52
# [WORKER 1] Completed work in 3s
# --- File: ./logs/threads/worker_2.log ---
# [WORKER 2] Task started at 18:29:52
# [WORKER 2] Completed work in 3s
# --- File: ./logs/threads/worker_3.log ---
# [WORKER 3] Task started at 18:29:52
# [WORKER 3] Completed work in 2s
# --- File: ./logs/threads/worker_4.log ---
# [WORKER 4] Task started at 18:29:52
# [WORKER 4] Completed work in 3s
# [SUCCESS] All parallel tasks synchronized successfully.
# Finished: SUCCESS