#!/bin/bash
NETWORK_NAME="NET_test_3"
SUBNET="172.28.1.0/24"

docker network create \
    --driver bridge \
    --subnet $SUBNET \
    $NETWORK_NAME

echo "Нажми Enter, чтобы продолжить..."
read # Аналог Pause в Linux
docker network ls

echo "Нажми Enter, чтобы проверить детали сети..."
read
docker network inspect $NETWORK_NAME