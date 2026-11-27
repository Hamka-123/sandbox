#!/usr/bin/env bash
set -Eeuo pipefail

# End-to-end Stateful app migration: Minikube -> Azure Blob/Velero -> AKS.
# Run from the repository root, or set PROJECT_DIR to the repository path.

PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"
TF_DIR="${TF_DIR:-$PROJECT_DIR/velero-aks}"
MANIFEST_DIR="${MANIFEST_DIR:-$PROJECT_DIR/k8s}"
NAMESPACE="${NAMESPACE:-migration}"
APP_DEPLOYMENT="${APP_DEPLOYMENT:-hellogo-deployment}"
APP_SERVICE="${APP_SERVICE:-hellogo-service}"
BACKUP_NAME="${BACKUP_NAME:-migration-backup}"
MINIKUBE_CONTEXT="${MINIKUBE_CONTEXT:-minikube}"
OWNER="${OWNER:-}"
AKS_CONTEXT="${AKS_CONTEXT:-}"
RUN_DESTROY=false
SKIP_INSTALLS=false
PORT_FORWARD=false
DATE_FILE="/data/date.txt"

log()  { printf '\n\033[1;34m[INFO]\033[0m %s\n' "$*"; }
warn() { printf '\n\033[1;33m[WARN]\033[0m %s\n' "$*" >&2; }
die()  { printf '\n\033[1;31m[ERROR]\033[0m %s\n' "$*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "Required command not found: $1"; }

usage() {
  cat <<'EOF'
Usage: ./migrate-stateful.sh [options]

Options:
  --project-dir PATH  Repository root (default: current directory)
  --owner VALUE       Owner suffix used in AKS context/resource-group naming
  --aks-context NAME  Explicit AKS kubeconfig context (recommended)
  --destroy           After verification, ask before terraform destroy
  --skip-install      Skip Homebrew/tool installation checks
  --port-forward      Start kubectl port-forward at the end (foreground)
  -h, --help          Show this help

Environment overrides:
  TF_DIR, MANIFEST_DIR, NAMESPACE, APP_DEPLOYMENT, APP_SERVICE,
  BACKUP_NAME, MINIKUBE_CONTEXT, OWNER, AKS_CONTEXT
EOF
}

while (($#)); do
  case "$1" in
    --project-dir) PROJECT_DIR="${2:?Missing path}"; shift 2 ;;
    --owner) OWNER="${2:?Missing owner}"; shift 2 ;;
    --aks-context) AKS_CONTEXT="${2:?Missing context}"; shift 2 ;;
    --destroy) RUN_DESTROY=true; shift ;;
    --skip-install) SKIP_INSTALLS=true; shift ;;
    --port-forward) PORT_FORWARD=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die "Unknown option: $1 (use --help)" ;;
  esac
done

TF_DIR="${TF_DIR:-$PROJECT_DIR/velero-aks}"
MANIFEST_DIR="${MANIFEST_DIR:-$PROJECT_DIR/manifests}"

[[ -d "$TF_DIR" ]] || die "Terraform directory not found: $TF_DIR"
[[ -d "$MANIFEST_DIR" ]] || die "Manifest directory not found: $MANIFEST_DIR"

if [[ "$SKIP_INSTALLS" == false ]]; then
  need brew
  log "Installing/checking local tools with Homebrew"
  brew list minikube >/dev/null 2>&1 || brew install minikube
  brew list velero >/dev/null 2>&1 || brew install velero
  brew list kubectl >/dev/null 2>&1 || brew install kubectl
  brew list terraform >/dev/null 2>&1 || brew install terraform
  brew list azure-cli >/dev/null 2>&1 || brew install azure-cli
fi

for cmd in minikube velero kubectl terraform az; do need "$cmd"; done

log "Checking Azure login"
if ! az account show >/dev/null 2>&1; then
  az login
fi

log "Starting Minikube"
if ! minikube status >/dev/null 2>&1; then
  minikube start --addons=csi-hostpath-driver,volumesnapshots --driver=docker
fi
kubectl cluster-info --context "$MINIKUBE_CONTEXT" >/dev/null

log "Initializing and applying Terraform infrastructure"
cd "$TF_DIR"
terraform init
terraform validate
terraform apply

for output_name in velero_install_minikube aks_get_credentials velero_install_aks; do
  terraform output -raw "$output_name" >/dev/null 2>&1 ||
    die "Missing Terraform output: $output_name"
done

log "Applying Kubernetes manifests to Minikube"
kubectl apply -f "$MANIFEST_DIR/" --context "$MINIKUBE_CONTEXT"

log "Waiting for application deployment in Minikube"
kubectl rollout status "deployment/$APP_DEPLOYMENT" \
  -n "$NAMESPACE" --context "$MINIKUBE_CONTEXT" --timeout=180s

log "Writing a migration marker to the persistent volume"
kubectl exec "deployment/$APP_DEPLOYMENT" -n "$NAMESPACE" \
  --context "$MINIKUBE_CONTEXT" -- sh -c "date -u +%Y-%m-%dT%H:%M:%SZ > '$DATE_FILE'"
SOURCE_MARKER="$(kubectl exec "deployment/$APP_DEPLOYMENT" -n "$NAMESPACE" \
  --context "$MINIKUBE_CONTEXT" -- cat "$DATE_FILE" | tr -d '\r')"
[[ -n "$SOURCE_MARKER" ]] || die "Could not read migration marker from Minikube"
log "Source marker: $SOURCE_MARKER"

log "Installing Velero in Minikube using Terraform output"
INSTALL_MINIKUBE="$(terraform output -raw velero_install_minikube)"
bash -c "$INSTALL_MINIKUBE"

log "Waiting for Velero backup storage location"
for attempt in {1..30}; do
  if velero backup-location get --kubecontext "$MINIKUBE_CONTEXT" 2>/dev/null |
      grep -q 'Available'; then
    break
  fi
  if [[ "$attempt" -eq 30 ]]; then
    velero backup-location get --kubecontext "$MINIKUBE_CONTEXT" || true
    die "Velero backup storage location did not become Available"
  fi
  sleep 10
done

log "Creating backup: $BACKUP_NAME"
if velero backup get "$BACKUP_NAME" --kubecontext "$MINIKUBE_CONTEXT" >/dev/null 2>&1; then
  warn "Backup $BACKUP_NAME already exists. Choose a new BACKUP_NAME to avoid ambiguity."
  die "Refusing to reuse an existing backup name"
fi

velero backup create "$BACKUP_NAME" \
  --include-namespaces "$NAMESPACE" \
  --kubecontext "$MINIKUBE_CONTEXT" \
  --wait

log "Verifying backup details"
velero backup describe "$BACKUP_NAME" --details --kubecontext "$MINIKUBE_CONTEXT"

log "Getting AKS credentials using Terraform output"
eval "$(terraform output -raw aks_get_credentials)"

if [[ -z "$AKS_CONTEXT" ]]; then
  AKS_CONTEXT="$(kubectl config get-contexts -o name | grep -E 'aks|velero' | head -n 1)"
  [[ -n "$AKS_CONTEXT" ]] || die "Could not detect AKS context automatically. Pass --aks-context <name>"
fi
log "Using AKS context: $AKS_CONTEXT"

log "Installing Velero in AKS using Terraform output"
INSTALL_AKS="$(terraform output -raw velero_install_aks)"
bash -c "$INSTALL_AKS"

log "Restoring application into AKS from backup: $BACKUP_NAME"
velero restore create --from-backup "$BACKUP_NAME" \
  --kubecontext "$AKS_CONTEXT" \
  --wait

log "Waiting for application deployment in AKS"
kubectl rollout status "deployment/$APP_DEPLOYMENT" \
  -n "$NAMESPACE" --context "$AKS_CONTEXT" --timeout=300s

log "Verifying migration marker on the AKS persistent volume"
DEST_MARKER="$(kubectl exec "deployment/$APP_DEPLOYMENT" -n "$NAMESPACE" \
  --context "$AKS_CONTEXT" -- cat "$DATE_FILE" | tr -d '\r')"
log "Source marker (Minikube): $SOURCE_MARKER"
log "Dest marker (AKS):       $DEST_MARKER"

if [[ "$SOURCE_MARKER" == "$DEST_MARKER" ]]; then
  log "SUCCESS: Persistent volume data successfully migrated and verified!"
else
  die "VERIFICATION FAILED: Data markers do not match!"
fi

if [[ "$PORT_FORWARD" == true ]]; then
  log "Starting port-forwarding to $APP_SERVICE on http://localhost:8080 (Ctrl+C to stop)"
  kubectl port-forward "svc/$APP_SERVICE" 8080:80 -n "$NAMESPACE" --context "$AKS_CONTEXT"
fi

if [[ "$RUN_DESTROY" == true ]]; then
  warn "Preparing to destroy infrastructure (--destroy requested)"
  read -rp "Are you sure you want to run terraform destroy and wipe resources? [y/N] " confirm
  if [[ "$confirm" =~ ^[Yy]$ ]]; then
    log "Uninstalling Velero from Minikube"
    velero uninstall --kubecontext "$MINIKUBE_CONTEXT" --force || true
    
    log "Deleting namespace in Minikube"
    kubectl --context "$MINIKUBE_CONTEXT" delete namespace "$NAMESPACE" --ignore-not-found || true

    log "Running terraform destroy"
    cd "$TF_DIR"
    terraform destroy -auto-approve
    
    log "Cleaning up AKS context from kubeconfig"
    [[ -n "$AKS_CONTEXT" ]] && kubectl config delete-context "$AKS_CONTEXT" || true
    
    log "Cleanup completed."
  else
    log "Destruction skipped by user."
  fi
else
  log "Migration completed successfully! Cloud resources were kept. Use --destroy to clean up automatically."
fi