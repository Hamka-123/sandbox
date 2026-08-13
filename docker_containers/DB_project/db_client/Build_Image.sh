#!/bin/bash

CONTAINER_NAME="client_v1.0"
IMAGE_NAME="python_client:v1.0"
DOCKERFILE="./Dockerfile"
CONTEXT="."

# 0. Удаляем контейнер (нельзя удалить образ, пока живой контейнер, который его использует)
if [ "$(docker ps -aq -f name=^/${CONTAINER_NAME}$)" ]; then
    echo "--- Удаляем старый контейнер $CONTAINER_NAME ---"
    docker rm -f $CONTAINER_NAME
fi

# 1. Проверяем наличие образа и удаляем его
if [ "$(docker images -q $IMAGE_NAME)" ]; then
    echo "--- Образ $IMAGE_NAME найден. Удаляем... ---"
    docker rmi -f $IMAGE_NAME
else
    echo "--- Образ $IMAGE_NAME не найден, начинаем чистую сборку ---"
fi

# 2. Билдим новый образ
echo "--- Сборка нового образа $IMAGE_NAME ---"
docker build \
    --pull \
    --rm \
    -f "$DOCKERFILE" \
    -t "$IMAGE_NAME" \
    "$CONTEXT"

echo "--- Готово! Образ обновлен. ---"