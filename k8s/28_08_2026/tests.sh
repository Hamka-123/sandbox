#! /bin/bash
set -e

# tests

curl http://local.app.test/
# Или через портофорвард для теста:
kubectl port-forward svc/frontend-service 8080:80 -n app-ns
curl http://localhost:8080


kubectl port-forward svc/backend-service 9090:80 -n app-ns
curl http://localhost:9090  # Запрос зависнет или получит тайм-аут (Connection refused / timed out)


kubectl exec -it deployment/frontend-deployment -n app-ns -- sh
# Внутри контейнера:
wget -qO- http://backend-service
# Должен вернуть: Hello from Backend!