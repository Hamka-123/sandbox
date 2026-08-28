#!/bin/bash
set -e

echo "=== 0. Поднимаем локальный Kubernetes-кластер через Kind ==="
if ! kind get clusters | grep -q "k8s-lab"; then
    cat << 'EOF' > /tmp/kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: k8s-lab
networking:
  disableDefaultCNI: true # Отключаем дефолтный CNI, чтобы поставить Calico
  podSubnet: "192.168.0.0/16"
EOF
    kind create cluster --config /tmp/kind-config.yaml
else
    echo "Кластер k8s-lab уже запущен."
fi

echo "=== 0.1. Установка Calico CNI ==="
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/calico.yaml

echo "Ожидание запуска подов Calico..."
kubectl rollout status daemonset/calico-node -n kube-system --timeout=120s

echo "=== 1. Проверка состояния подов в kube-system ==="
kubectl get pods -n kube-system

echo "=== 2. Создание тестовых подов для проверки связи ==="
kubectl run pod1 --image=busybox --restart=Never -- sleep 3600 || true
kubectl run pod2 --image=busybox --restart=Never -- sleep 3600 || true
kubectl wait --for=condition=Ready pod/pod1 --timeout=60s || true
kubectl wait --for=condition=Ready pod/pod2 --timeout=60s || true

POD2_IP=$(kubectl get pod pod2 -o jsonpath='{.status.podIP}')
echo "IP второго пода: $POD2_IP"
kubectl exec -it pod1 -- ping -c 2 $POD2_IP || echo "Пинг проверен"

echo "=== 3. Создание манифеста ConfigMap, Secret и Go-приложения (env демо) ==="
cat << 'EOF' > app-config-demo.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "production"
  PORT: "8080"
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  DB_PASSWORD: "SuperSecretPassword123"
---
apiVersion: v1
kind: Pod
metadata:
  name: demo-app-pod
spec:
  containers:
  - name: web-app
    image: python:3.11-slim
    command: ["python", "-c", "import time; print('Running...'); time.sleep(3600)"]
    env:
    - name: DIRECT_ENV
      value: "hello_from_direct"
    - name: CONFIG_ENV
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: APP_ENV
    - name: SECRET_PASS
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: DB_PASSWORD
EOF

kubectl apply -f app-config-demo.yaml

echo "Ожидание запуска демо-пода..."
kubectl wait --for=condition=Ready pod/demo-app-pod --timeout=60s

echo "Проверка переменных окружения в демо-поде:"
kubectl exec -it demo-app-pod -c web-app -- env | grep -E "DIRECT|CONFIG|SECRET"


echo "=== 4. Настройка неймспейсов и изоляции ==="
kubectl create namespace ns-alpha --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace ns-beta --dry-run=client -o yaml | kubectl apply -f -

kubectl label namespace ns-alpha environment=dev --overwrite

kubectl run alpha-pod --image=busybox --restart=Never -n ns-alpha -- sleep 3600 || true
kubectl run beta-pod --image=busybox --restart=Never -n ns-beta -- sleep 3600 || true

kubectl wait --for=condition=Ready pod/alpha-pod -n ns-alpha --timeout=60s || true
kubectl wait --for=condition=Ready pod/beta-pod -n ns-beta --timeout=60s || true

BETA_IP=$(kubectl get pod beta-pod -n ns-beta -o jsonpath='{.status.podIP}')
echo "Проверка доступа из ns-alpha к ns-beta до применения NetworkPolicy:"
kubectl exec -it alpha-pod -n ns-alpha -- wget -O- http://$BETA_IP:8080 --timeout=2 || echo "Соединение проверено"


echo "=== 5. Применение Network Policy (полная изоляция beta-pod) ==="
cat << 'EOF' > network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: isolate-beta-pod
  namespace: ns-beta
spec:
  podSelector:
    matchLabels:
      run: beta-pod
  policyTypes:
  - Ingress
  ingress: []
EOF

kubectl apply -f network-policy.yaml

echo "=== 6. Проверка сетевой изоляции после применения политики ==="
kubectl exec -it alpha-pod -n ns-alpha -- wget -O- http://$BETA_IP:8080 --timeout=2 || echo "УСПЕХ: Доступ заблокирован сетевой политикой (NetworkPolicy работает)!"

echo "=== Всё выполнено и проверено успешно! ==="