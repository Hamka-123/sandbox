#! /bin/bash
set -e

echo "Starting Docker Desktop..."
open -a Docker
# Ждем 10 секунд, пока демон Docker точно инициализируется
sleep 10

minikube version
minikube start

echo "Enabling Ingress addon..."
minikube addons enable ingress
kubectl get pods -n ingress-nginx

echo "Creating namespace and applying manifests..."
kubectl create namespace app-ns || true # Если неймспейс уже есть, скрипт не упадет

kubectl apply -f app-deployment.yaml
kubectl apply -f network-policies.yaml
echo "Waiting for ingress webhook to be ready..."
# Ждем, пока эндпоинт вебхука начнет отвечать (таймаут 30 секунд)
for i in {1..15}; do
  if kubectl get endpoints ingress-nginx-controller-admission -n ingress-nginx &>/dev/null; then
    echo "Webhook is ready!"
    break
  fi
  sleep 2
done

echo "Applying ingress..."
kubectl apply -f ingress.yaml

echo "Deployment finished successfully!"
