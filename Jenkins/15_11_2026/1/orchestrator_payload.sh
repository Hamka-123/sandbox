#!/usr/bin/env bash
set -euo pipefail

JENKINS_URL="http://localhost:8080"
CHILD_JOB="lesson9-audit-worker"
ENV_CHOICE="${TARGET_ENV:-staging}"
SIMULATE_FAIL="${FORCE_FAIL:-false}"
TRACKING_ID="ORD-${BUILD_NUMBER}-$(date +%s)"

echo "=========================================================="
echo "  LESSON 9 ORCHESTRATOR (BUILD #${BUILD_NUMBER})"
echo "=========================================================="

# 1. Obtain CSRF Crumb cleanly
CRUMB=$(curl -s -u "admin:" \
  "${JENKINS_URL}/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)" 2>/dev/null || true)

# 2. Trigger parameterized child job and capture response headers
echo "--> Triggering '${CHILD_JOB}' [ENV=${ENV_CHOICE}, FAIL=${SIMULATE_FAIL}, ID=${TRACKING_ID}]..."
HEADER_FILE="/tmp/headers_${BUILD_NUMBER}.txt"

TRIGGER_URL="${JENKINS_URL}/job/${CHILD_JOB}/buildWithParameters?TARGET_ENV=${ENV_CHOICE}&REQUEST_ID=${TRACKING_ID}&FORCE_FAIL=${SIMULATE_FAIL}"

if [ -n "${CRUMB}" ]; then
    curl -s -D "${HEADER_FILE}" -X POST -H "${CRUMB}" -u "admin:" "${TRIGGER_URL}" > /dev/null
else
    curl -s -D "${HEADER_FILE}" -X POST -u "admin:" "${TRIGGER_URL}" > /dev/null
fi

HTTP_STATUS=$(grep -i "^HTTP/" "${HEADER_FILE}" | tail -n 1 | awk '{print $2}' | tr -d '\r\n')
QUEUE_URL=$(grep -i "^Location:" "${HEADER_FILE}" | awk '{print $2}' | tr -d '\r\n')
rm -f "${HEADER_FILE}"

if [ "${HTTP_STATUS}" != "201" ] || [ -z "${QUEUE_URL}" ]; then
    echo "[ERROR] Trigger failed! HTTP Status: ${HTTP_STATUS}"
    exit 1
fi

echo "--> Queue Item Created: ${QUEUE_URL}"

# 3. Poll Queue State Machine until executable number is assigned
CHILD_BUILD_NUM=""
WAIT_SECONDS=0
MAX_QUEUE_WAIT=45

while [ -z "${CHILD_BUILD_NUM}" ]; do
    if [ "${WAIT_SECONDS}" -ge "${MAX_QUEUE_WAIT}" ]; then
        echo "[ERROR] Timed out waiting in queue after ${MAX_QUEUE_WAIT}s."
        exit 1
    fi

    QUEUE_JSON=$(curl -s -u "admin:" "${QUEUE_URL}api/json")

    # Check if item was cancelled while queued
    IS_CANCELLED=$(echo "${QUEUE_JSON}" | python3 -c 'import sys, json; print(json.load(sys.stdin).get("cancelled", False))' 2>/dev/null || echo "False")
    if [ "${IS_CANCELLED}" = "True" ]; then
        echo "[ERROR] Downstream job was cancelled while in queue!"
        exit 1
    fi

    CHILD_BUILD_NUM=$(echo "${QUEUE_JSON}" | python3 -c 'import sys, json; exe=json.load(sys.stdin).get("executable"); print(exe.get("number") if exe else "")' 2>/dev/null || true)

    if [ -z "${CHILD_BUILD_NUM}" ]; then
        sleep 1
        WAIT_SECONDS=$((WAIT_SECONDS + 1))
    fi
done

echo "--> Executor Assigned! Child Build #${CHILD_BUILD_NUM} is active."

# 4. Poll Build Execution until building == false
while true; do
    BUILD_JSON=$(curl -s -u "admin:" "${JENKINS_URL}/job/${CHILD_JOB}/${CHILD_BUILD_NUM}/api/json")
    IS_BUILDING=$(echo "${BUILD_JSON}" | python3 -c 'import sys, json; print(json.load(sys.stdin).get("building", True))')

    if [ "${IS_BUILDING}" = "False" ]; then
        BUILD_RESULT=$(echo "${BUILD_JSON}" | python3 -c 'import sys, json; print(json.load(sys.stdin).get("result", "UNKNOWN"))')
        echo "--> Child Build #${CHILD_BUILD_NUM} Finished with Result: ${BUILD_RESULT}"
        break
    fi
    sleep 2
done

# 5. Propagate Failure if Child Did Not Succeed
if [ "${BUILD_RESULT}" != "SUCCESS" ]; then
    echo "[ERROR] Downstream job failed (${BUILD_RESULT}). Aborting parent pipeline."
    exit 1
fi

# 6. Retrieve & Validate Artifact over REST
ARTIFACT_URL="${JENKINS_URL}/job/${CHILD_JOB}/${CHILD_BUILD_NUM}/artifact/audit_report.json"
curl -s -f -u "admin:" -o "ingested_audit.json" "${ARTIFACT_URL}"

echo "=========================================================="
echo "  VERIFIED ARTIFACT PAYLOAD (ingested_audit.json)"
echo "=========================================================="
cat ingested_audit.json
echo ""

# Verify tracking ID round-trip
RETURNED_ID=$(python3 -c 'import json; print(json.load(open("ingested_audit.json")).get("request_id"))')
if [ "${RETURNED_ID}" != "${TRACKING_ID}" ]; then
    echo "[ERROR] Artifact mismatch! Expected ${TRACKING_ID}, got ${RETURNED_ID}"
    exit 1
fi

echo "[SUCCESS] Round-trip correlation ID (${RETURNED_ID}) verified!"
