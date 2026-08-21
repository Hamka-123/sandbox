#!/bin/bash
set -e
kubectl apply -f deployment.yaml --record=true
kubectl rollout status deployment/web-app

echo "=== [1/4] Обновляем деплоймент до v2 (вызываем ролаут) ==="
kubectl set image deployment/web-app nginx=nginx:1.16.1 --record=true
kubectl rollout status deployment/web-app

echo "=== [2/4] Проверяем историю ревизий ==="
kubectl rollout history deployment/web-app

echo "=== [3/4] Откатываемся на предыдущую версию (v1) ==="
kubectl rollout undo deployment/web-app
kubectl rollout status deployment/web-app
kubectl rollout history deployment/web-app

echo "=== [4/4] Тестируем стратегию Recreate ==="
# Сначала патчим тип на Recreate и удаляем мешающие настройки rollingUpdate
kubectl patch deployment web-app --type='json' -p='[
  {"op": "replace", "path": "/spec/strategy/type", "value": "Recreate"},
  {"op": "remove", "path": "/spec/strategy/rollingUpdate"}
]'

# Обновляем образ, чтобы запустить деплоймент с новой стратегией
kubectl set image deployment/web-app nginx=nginx:latest --record=true
kubectl rollout status deployment/web-app
echo "Готово! Часть 1 успешно выполнена."