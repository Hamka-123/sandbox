#!/bin/bash
set -e

kubectl apply -f pods-probes.yaml

echo "Ожидаем поднятия пода и проверяем статус..."
sleep 5
kubectl describe pod probe-demo-pod

echo "Готово! Часть 2 развернута. Можете понаблюдать за подами через: kubectl get pods -w"
