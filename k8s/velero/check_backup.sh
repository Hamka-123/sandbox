#!/usr/bin/env bash
set -Eeuo pipefail

# ============================================================
# Configuration
# ============================================================

SOURCE_CONTEXT="minikube"
SOURCE_NS="migration"
PVC_NAME="app-pvc"
VELERO_NS="velero"

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_NAME="migration-check-${TIMESTAMP}"
RESTORE_NAME="migration-restore-${TIMESTAMP}"
TEST_NS="migration-verify-${TIMESTAMP}"

CHECKER_IMAGE="busybox:1.36"
CHECKER_POD="pvc-checker"

WORK_DIR="$(mktemp -d)"
BASELINE_FILE="${WORK_DIR}/source.sha256"
RESTORED_FILE="${WORK_DIR}/restored.sha256"
BACKUP_LOG="${WORK_DIR}/backup.log"
RESTORE_LOG="${WORK_DIR}/restore.log"

# ============================================================
# Helpers
# ============================================================

log() {
    printf '\n[%s] %s\n' "$(date '+%H:%M:%S')" "$*"
}

fail() {
    echo
    echo "❌ ERROR: $*" >&2
    echo "Temporary files: ${WORK_DIR}" >&2
    exit 1
}

cleanup() {
    # Delete temporary checker Pods.
    kubectl --context "$SOURCE_CONTEXT" \
        -n "$SOURCE_NS" delete pod "$CHECKER_POD" \
        --ignore-not-found --wait=false >/dev/null 2>&1 || true

    kubectl --context "$SOURCE_CONTEXT" \
        -n "$TEST_NS" delete pod "$CHECKER_POD" \
        --ignore-not-found --wait=false >/dev/null 2>&1 || true
}

on_exit() {
    local exit_code=$?
    cleanup

    if [[ "$exit_code" -eq 0 ]]; then
        rm -rf "$WORK_DIR"
    else
        echo "Diagnostic files retained in: ${WORK_DIR}" >&2
    fi
}
trap on_exit EXIT

require_command() {
    command -v "$1" >/dev/null 2>&1 ||
        fail "Required command not found: $1"
}

# ============================================================
# Check prerequisites
# ============================================================

log "Checking required tools..."

for cmd in kubectl velero jq sha256sum diff; do
    require_command "$cmd"
done

kubectl --context "$SOURCE_CONTEXT" \
    get namespace "$SOURCE_NS" >/dev/null ||
    fail "Source namespace '$SOURCE_NS' not found in context '$SOURCE_CONTEXT'"

kubectl --context "$SOURCE_CONTEXT" \
    -n "$VELERO_NS" get deployment velero >/dev/null ||
    fail "Velero deployment not found in namespace '$VELERO_NS'"

kubectl --context "$SOURCE_CONTEXT" \
    -n "$SOURCE_NS" get pvc "$PVC_NAME" >/dev/null ||
    fail "Source PVC '$PVC_NAME' not found"

PVC_PHASE="$(
    kubectl --context "$SOURCE_CONTEXT" \
        -n "$SOURCE_NS" get pvc "$PVC_NAME" \
        -o jsonpath='{.status.phase}'
)"

[[ "$PVC_PHASE" == "Bound" ]] ||
    fail "Source PVC is not Bound (status: ${PVC_PHASE:-unknown})"

# ============================================================
# Snapshot helper
# ============================================================

snapshot_pvc() {
    local namespace="$1"
    local pvc="$2"
    local output_file="$3"

    log "Calculating checksums: namespace=$namespace, PVC=$pvc"

    # Remove a stale helper Pod from a previous run.
    kubectl --context "$SOURCE_CONTEXT" \
        -n "$namespace" delete pod "$CHECKER_POD" \
        --ignore-not-found --wait=true >/dev/null

    kubectl --context "$SOURCE_CONTEXT" \
        -n "$namespace" apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: ${CHECKER_POD}
spec:
  restartPolicy: Never
  containers:
    - name: checker
      image: ${CHECKER_IMAGE}
      command: ["sh", "-c", "sleep 3600"]
      volumeMounts:
        - name: data
          mountPath: /data
          readOnly: true
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: ${pvc}
        readOnly: true
EOF

    if ! kubectl --context "$SOURCE_CONTEXT" \
        -n "$namespace" wait \
        --for=condition=Ready "pod/$CHECKER_POD" \
        --timeout=180s; then

        kubectl --context "$SOURCE_CONTEXT" \
            -n "$namespace" describe pod "$CHECKER_POD" || true

        kubectl --context "$SOURCE_CONTEXT" \
            -n "$namespace" logs "$CHECKER_POD" || true

        fail "Unable to start the PVC checker Pod in namespace '$namespace'"
    fi

    kubectl --context "$SOURCE_CONTEXT" \
        -n "$namespace" exec "$CHECKER_POD" -- sh -c '
            set -eu
            cd /data
            find . -type f -exec sha256sum {} \; | sort
        ' > "$output_file" ||
        fail "Could not calculate file checksums in namespace '$namespace'"

    kubectl --context "$SOURCE_CONTEXT" \
        -n "$namespace" delete pod "$CHECKER_POD" \
        --wait=true --timeout=60s >/dev/null ||
        fail "Could not remove the checker Pod in namespace '$namespace'"

    log "Files found: $(wc -l < "$output_file" | tr -d ' ')"
}

# ============================================================
# 1. Capture source data BEFORE backup
# ============================================================

log "Step 1/7: Capturing the source PVC baseline..."

snapshot_pvc "$SOURCE_NS" "$PVC_NAME" "$BASELINE_FILE"

# ============================================================
# 2. Create a fresh Velero backup
# ============================================================

log "Step 2/7: Creating backup '$BACKUP_NAME'..."

velero --kubecontext "$SOURCE_CONTEXT" \
    backup create "$BACKUP_NAME" \
    --include-namespaces "$SOURCE_NS" \
    --wait 2>&1 | tee "$BACKUP_LOG"

BACKUP_PHASE="$(
    velero --kubecontext "$SOURCE_CONTEXT" \
        backup get "$BACKUP_NAME" -o json |
        jq -r '.status.phase // "Unknown"'
)"

[[ "$BACKUP_PHASE" == "Completed" ]] ||
    fail "Backup did not complete successfully (phase: $BACKUP_PHASE)"

BACKUP_ERRORS="$(
    velero --kubecontext "$SOURCE_CONTEXT" \
        backup get "$BACKUP_NAME" -o json |
        jq -r '.status.errors // 0'
)"

BACKUP_WARNINGS="$(
    velero --kubecontext "$SOURCE_CONTEXT" \
        backup get "$BACKUP_NAME" -o json |
        jq -r '.status.warnings // 0'
)"

log "Backup phase: $BACKUP_PHASE"
log "Backup errors: $BACKUP_ERRORS"
log "Backup warnings: $BACKUP_WARNINGS"

[[ "$BACKUP_ERRORS" == "0" ]] ||
    fail "Velero reports backup errors: $BACKUP_ERRORS"

# ============================================================
# 3. Inspect backup logs and volume operations
# ============================================================

log "Step 3/7: Checking backup logs..."

velero --kubecontext "$SOURCE_CONTEXT" \
    backup logs "$BACKUP_NAME" > "$WORK_DIR/backup-details.log" 2>&1 ||
    fail "Unable to retrieve backup logs"

if grep -Ein '(^|[^[:alpha:]])(error|fatal)([^[:alpha:]]|$)' \
    "$WORK_DIR/backup-details.log"; then
    fail "Potential errors found in backup logs; inspect the output above"
fi

log "Backup logs contain no obvious error/fatal entries."

log "Checking PodVolumeBackup operations, if applicable..."

if kubectl --context "$SOURCE_CONTEXT" \
    -n "$VELERO_NS" get crd podvolumebackups.velero.io >/dev/null 2>&1; then

    PVB_JSON="$(
        kubectl --context "$SOURCE_CONTEXT" \
            -n "$VELERO_NS" get podvolumebackups \
            -l "velero.io/backup-name=$BACKUP_NAME" \
            -o json
    )"

    PVB_COUNT="$(jq '.items | length' <<< "$PVB_JSON")"

    if [[ "$PVB_COUNT" -gt 0 ]]; then
        jq -r '.items[] |
            "\(.metadata.name): \(.status.phase // "Unknown")"' \
            <<< "$PVB_JSON"

        FAILED_PVB="$(
            jq '[.items[] |
                select((.status.phase // "") != "Completed")] | length' \
                <<< "$PVB_JSON"
        )"

        [[ "$FAILED_PVB" == "0" ]] ||
            fail "One or more PodVolumeBackup operations are not Completed"
    else
        echo "No PodVolumeBackup objects found for this backup."
        echo "This is not automatically an error: the setup may use CSI snapshots or another data mover."
    fi
else
    echo "PodVolumeBackup CRD is not installed; skipping this check."
fi

# ============================================================
# 4. Restore into a separate namespace
# ============================================================

log "Step 4/7: Creating isolated test namespace '$TEST_NS'..."

kubectl --context "$SOURCE_CONTEXT" \
    create namespace "$TEST_NS" >/dev/null ||
    fail "Could not create test namespace '$TEST_NS'"

log "Restoring backup '$BACKUP_NAME'..."

velero --kubecontext "$SOURCE_CONTEXT" \
    restore create "$RESTORE_NAME" \
    --from-backup "$BACKUP_NAME" \
    --namespace-mappings "${SOURCE_NS}:${TEST_NS}" \
    --wait 2>&1 | tee "$RESTORE_LOG"

RESTORE_PHASE="$(
    velero --kubecontext "$SOURCE_CONTEXT" \
        restore get "$RESTORE_NAME" -o json |
        jq -r '.status.phase // "Unknown"'
)"

[[ "$RESTORE_PHASE" == "Completed" ]] ||
    fail "Restore did not complete successfully (phase: $RESTORE_PHASE)"

RESTORE_ERRORS="$(
    velero --kubecontext "$SOURCE_CONTEXT" \
        restore get "$RESTORE_NAME" -o json |
        jq -r '.status.errors // 0'
)"

RESTORE_WARNINGS="$(
    velero --kubecontext "$SOURCE_CONTEXT" \
        restore get "$RESTORE_NAME" -o json |
        jq -r '.status.warnings // 0'
)"

log "Restore phase: $RESTORE_PHASE"
log "Restore errors: $RESTORE_ERRORS"
log "Restore warnings: $RESTORE_WARNINGS"

[[ "$RESTORE_ERRORS" == "0" ]] ||
    fail "Velero reports restore errors: $RESTORE_ERRORS"

# ============================================================
# 5. Verify the restored PVC
# ============================================================

log "Step 5/7: Waiting for restored PVC '$PVC_NAME'..."

for attempt in $(seq 1 60); do
    RESTORED_PVC_PHASE="$(
        kubectl --context "$SOURCE_CONTEXT" \
            -n "$TEST_NS" get pvc "$PVC_NAME" \
            -o jsonpath='{.status.phase}' 2>/dev/null || true
    )"

    if [[ "$RESTORED_PVC_PHASE" == "Bound" ]]; then
        break
    fi

    sleep 5
done

[[ "${RESTORED_PVC_PHASE:-}" == "Bound" ]] ||
    fail "Restored PVC did not become Bound (status: ${RESTORED_PVC_PHASE:-not found})"

kubectl --context "$SOURCE_CONTEXT" \
    -n "$TEST_NS" get pvc "$PVC_NAME" -o wide

# Check PodVolumeRestore operations if this mechanism is present.
if kubectl --context "$SOURCE_CONTEXT" \
    -n "$VELERO_NS" get crd podvolumerestores.velero.io >/dev/null 2>&1; then

    PVR_JSON="$(
        kubectl --context "$SOURCE_CONTEXT" \
            -n "$VELERO_NS" get podvolumerestores \
            -l "velero.io/restore-name=$RESTORE_NAME" \
            -o json
    )"

    PVR_COUNT="$(jq '.items | length' <<< "$PVR_JSON")"

    if [[ "$PVR_COUNT" -gt 0 ]]; then
        jq -r '.items[] |
            "\(.metadata.name): \(.status.phase // "Unknown")"' \
            <<< "$PVR_JSON"

        FAILED_PVR="$(
            jq '[.items[] |
                select((.status.phase // "") != "Completed")] | length' \
                <<< "$PVR_JSON"
        )"

        [[ "$FAILED_PVR" == "0" ]] ||
            fail "One or more PodVolumeRestore operations are not Completed"
    else
        echo "No PodVolumeRestore objects found; this may be expected for the configured restore method."
    fi
fi

# ============================================================
# 6. Compare every file by SHA-256
# ============================================================

log "Step 6/7: Calculating checksums on the restored PVC..."

snapshot_pvc "$TEST_NS" "$PVC_NAME" "$RESTORED_FILE"

log "Comparing source baseline with restored files..."

if diff -u "$BASELINE_FILE" "$RESTORED_FILE"; then
    echo "✅ File lists and SHA-256 checksums match."
else
    fail "Restored files differ from the source baseline"
fi

# ============================================================
# 7. Result
# ============================================================

log "Step 7/7: Verification complete."

cat <<EOF

============================================================
✅ BACKUP AND RESTORE VERIFICATION PASSED
============================================================
Backup:       $BACKUP_NAME
Backup phase: $BACKUP_PHASE
Restore:      $RESTORE_NAME
Restore phase:$RESTORE_PHASE
Source PVC:   $SOURCE_NS/$PVC_NAME
Restored PVC: $TEST_NS/$PVC_NAME
Files checked: $(wc -l < "$BASELINE_FILE" | tr -d ' ')

The restored file list and SHA-256 checksums match the
baseline captured before the backup.
============================================================

EOF