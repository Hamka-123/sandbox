#!/bin/bash
set -e

kubectl apply -f svc-demo.yaml
kubectl rollout status deployment/svc-demo-deployment

echo "=== [1/3] Проверяем динамические Endpoints (должно быть 2 IP) ==="
kubectl get endpoints my-web-service

echo "=== [2/3] Меняем количество реплик до 4 и снова смотрим Endpoints ==="
kubectl scale deployment svc-demo-deployment --replicas=4
sleep 3
kubectl get endpoints my-web-service -o wide

echo "=== [3/3] Инструкция для Port-Forward ==="
echo "Для проверки доступа через браузер выполните в отдельном окне терминала:"
echo "  kubectl port-forward svc/my-web-service 8080:80"
echo "Затем откройте в браузере: http://localhost:8080"
echo "Запросы будут балансироваться между доступными подами (режим Round Robin со стороны Service)."

echo "Готово! Часть 3 успешно выполнена."