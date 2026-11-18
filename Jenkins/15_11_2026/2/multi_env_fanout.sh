#!/usr/bin/env bash
set -uo pipefail

JENKINS_URL="${JENKINS_URL:-http://localhost:8080}"
PARENT_JOB="lesson9-orchestrator"

declare -a RESULTS=()

for ENV in dev staging prod; do
    echo "=========================================================="
    echo "  DISPATCHING ${PARENT_JOB} FOR ENV=${ENV}"
    echo "=========================================================="

    HEADER_FILE="/tmp/fanout_headers_${ENV}_$$.txt"
    QUEUE_FILE="/tmp/fanout_queue_${ENV}_$$.json"
    BUILD_FILE="/tmp/fanout_build_${ENV}_$$.json"

    TRIGGER_URL="${JENKINS_URL}/job/${PARENT_JOB}/buildWithParameters?TARGET_ENV=${ENV}&FORCE_FAIL=false&_ts=$(date +%s)"
    HTTP_STATUS=$(curl -s -D "${HEADER_FILE}" -o /dev/null -w "%{http_code}" -X POST "${TRIGGER_URL}" || echo "000")

    QUEUE_URL=""
    if [ -f "${HEADER_FILE}" ]; then
        QUEUE_URL=$(grep -i "^Location:" "${HEADER_FILE}" | awk '{print $2}' | tr -d '\r\n' || true)
    fi

    if [ -z "${QUEUE_URL}" ]; then
        echo "[ERROR] Trigger failed for ENV=${ENV} (HTTP=${HTTP_STATUS})."
        RESULTS+=("N/A|${ENV}|FAILURE")
        continue
    fi

    QUEUE_URL="${QUEUE_URL%/}/"
    QUEUE_ID=$(echo "${QUEUE_URL}" | awk -F'/' '{for(i=NF;i>0;i--) if($i!="") {print $i; break}}')
    echo "--> Queue Item ID: ${QUEUE_ID}"

    PARENT_BUILD_NUM=""
    WAIT_SECONDS=0
    MAX_QUEUE_WAIT=30

    while [ -z "${PARENT_BUILD_NUM}" ]; do
        if [ "${WAIT_SECONDS}" -ge "${MAX_QUEUE_WAIT}" ]; then
            echo "[ERROR] Timed out waiting in queue for ENV=${ENV}."
            break
        fi

        Q_CODE=$(curl -s -o "${QUEUE_FILE}" -w "%{http_code}" "${QUEUE_URL}api/json" || echo "000")
        if [ "${Q_CODE}" = "200" ] && [ -s "${QUEUE_FILE}" ]; then
            PARENT_BUILD_NUM=$(grep -A 5 '"executable":' "${QUEUE_FILE}" 2>/dev/null | grep -o '"number":[0-9]*' | head -n 1 | cut -d: -f2 | tr -d '[:space:]' || true)
        fi

        if [ -z "${PARENT_BUILD_NUM}" ]; then
            curl -s "${JENKINS_URL}/job/${PARENT_JOB}/api/json?tree=builds[number,queueId]" -o "${BUILD_FILE}" || true
            if [ -s "${BUILD_FILE}" ]; then
                PARENT_BUILD_NUM=$(grep -B 1 -A 2 "\"queueId\":${QUEUE_ID}" "${BUILD_FILE}" 2>/dev/null | grep -o '"number":[0-9]*' | head -n 1 | cut -d: -f2 | tr -d '[:space:]' || true)
                if [ -z "${PARENT_BUILD_NUM}" ] && [ "${WAIT_SECONDS}" -ge 3 ]; then
                    PARENT_BUILD_NUM=$(grep -o '"number":[0-9]*' "${BUILD_FILE}" 2>/dev/null | head -n 1 | cut -d: -f2 | tr -d '[:space:]' || true)
                fi
            fi
        fi

        [ -z "${PARENT_BUILD_NUM}" ] && sleep 1 && WAIT_SECONDS=$((WAIT_SECONDS + 1))
    done

    if [ -z "${PARENT_BUILD_NUM}" ]; then
        RESULTS+=("N/A|${ENV}|FAILURE")
        continue
    fi

    echo "--> Parent Build #${PARENT_BUILD_NUM} running for ENV=${ENV}. Waiting for completion..."

    FINAL_RESULT="UNKNOWN"
    WAIT_BUILD=0
    while [ "${WAIT_BUILD}" -lt 60 ]; do
        # Запрашиваем ровно те поля, которые точно возвращают статус
        curl -s "${JENKINS_URL}/job/${PARENT_JOB}/${PARENT_BUILD_NUM}/api/json?tree=result,building" -o "${BUILD_FILE}" || true
        if [ -s "${BUILD_FILE}" ]; then
            IS_BUILDING=$(grep -o '"building":[^,}]*' "${BUILD_FILE}" 2>/dev/null | head -n 1 | cut -d: -f2 | tr -d '[:space:]' || true)
            if [ "${IS_BUILDING}" = "false" ]; then
                if grep -q '"result":"SUCCESS"' "${BUILD_FILE}"; then
                    FINAL_RESULT="SUCCESS"
                else
                    FINAL_RESULT="FAILURE"
                fi
                break
            fi
        fi
        sleep 3
        WAIT_BUILD=$((WAIT_BUILD + 1))
    done

    echo "--> ENV=${ENV} finished on Build #${PARENT_BUILD_NUM} with result: ${FINAL_RESULT}"
    RESULTS+=("#${PARENT_BUILD_NUM}|${ENV}|${FINAL_RESULT}")
done

echo ""
echo "=========================================================="
echo "  MULTI-ENVIRONMENT FAN-OUT SUMMARY"
echo "=========================================================="
printf "%-14s %-12s %-10s\n" "PARENT_BUILD" "ENV" "RESULT"
printf "%-14s %-12s %-10s\n" "------------" "---" "------"

for ENTRY in "${RESULTS[@]}"; do
    IFS='|' read -r B_NUM B_ENV B_RES <<< "${ENTRY}"
    printf "%-14s %-12s %-10s\n" "${B_NUM}" "${B_ENV}" "${B_RES}"
done