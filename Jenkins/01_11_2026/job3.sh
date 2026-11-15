#! /bin/bash 

cat << 'EOF' > script.groovy
import jenkins.model.*
import hudson.model.*
import hudson.tasks.Shell

def instance = Jenkins.get()
def jobName = 'lesson7-parallel-demo'
def job = instance.getItem(jobName)

String retryShellScript = '''#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo "  HOURS 5-6: NON-BLOCKING TRANSIENT RETRY LOOPS"
echo "=========================================================="

# Simulated unstable service invocation
unstable_service_call() {
    local attempt=$1
    # Succeeds on attempt 3
    if [ "${attempt}" -lt 3 ]; then
        echo "[SERVICE] Connection refused (HTTP 503 Service Unavailable)" >&2
        return 1
    fi
    echo "[SERVICE] HTTP 200 OK - Data synchronized successfully."
    return 0
}

# Generic retry wrapper function
retry_operation() {
    local max_attempts=$1
    local delay=$2
    local attempt=1
    local exit_code=0

    while [ "${attempt}" -le "${max_attempts}" ]; do
        echo "--> [ATTEMPT ${attempt}/${max_attempts}] Executing target operation..."
        
        # Disable set -e temporarily to evaluate subshell exit codes safely
        set +e
        unstable_service_call "${attempt}"
        exit_code=$?
        set -e

        if [ "${exit_code}" -eq 0 ]; then
            echo "[RETRY SUCCESS] Operation succeeded on attempt ${attempt}!"
            return 0
        fi

        echo "[RETRY WARNING] Attempt ${attempt} failed with exit code ${exit_code}." >&2
        if [ "${attempt}" -lt "${max_attempts}" ]; then
            echo "  [BACKOFF] Waiting ${delay}s before retry..."
            sleep "${delay}"
            # Exponential backoff calculation
            delay=$(( delay * 2 ))
        fi
        attempt=$(( attempt + 1 ))
    done

    echo "[RETRY FATAL] Operation failed after ${max_attempts} attempts." >&2
    return "${exit_code}"
}

# Execute operation with 4 max attempts, starting with a 1-second delay
retry_operation 4 1
'''

job.getBuildersList().clear()
job.getBuildersList().add(new Shell(retryShellScript))
job.save()

println "LESSON7_HOURS5_6_PROVISIONED"
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

# Wait for retries and backoff sleeps to finish
sleep 6

curl -s -u "admin:$API_TOKEN" "http://localhost:8080/job/lesson7-parallel-demo/${NEXT_BUILD_NUM}/consoleText"



# Started by user unknown or anonymous
# Running as SYSTEM
# Building in workspace /var/jenkins_home/workspace/lesson7-parallel-demo
# [lesson7-parallel-demo] $ /usr/bin/env bash /tmp/jenkins14242510359929116342.sh
# ==========================================================
#   HOURS 5-6: NON-BLOCKING TRANSIENT RETRY LOOPS
# ==========================================================
# --> [ATTEMPT 1/4] Executing target operation...
# [SERVICE] Connection refused (HTTP 503 Service Unavailable)
# [RETRY WARNING] Attempt 1 failed with exit code 1.
#   [BACKOFF] Waiting 1s before retry...
# --> [ATTEMPT 2/4] Executing target operation...
# [SERVICE] Connection refused (HTTP 503 Service Unavailable)
# [RETRY WARNING] Attempt 2 failed with exit code 1.
#   [BACKOFF] Waiting 2s before retry...
# --> [ATTEMPT 3/4] Executing target operation...
# [SERVICE] HTTP 200 OK - Data synchronized successfully.
# [RETRY SUCCESS] Operation succeeded on attempt 3!
# Finished: SUCCESS


