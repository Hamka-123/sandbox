#!/bin/bash

CONTAINER_NAME="db_client_v1.0"
IMAGE_NAME="python_client:v1.0"

# 0. Удаляем старый контейнер, если он завис
if [ "$(docker ps -aq -f name=^/${CONTAINER_NAME}$)" ]; then
    echo "--- Удаляем старый контейнер $CONTAINER_NAME ---"
    docker rm -f $CONTAINER_NAME
fi

# 1. Запуск и ВХОД (одновременно)
echo "--- Запуск и вход в контейнер $CONTAINER_NAME ---"
# Мы убираем -d, оставляем -it, чтобы сразу оказаться внутри
docker run -it --rm \
    --name $CONTAINER_NAME \
    $IMAGE_NAME /bin/bash 

# docker run -d --rm \
#     --name $CONTAINER_NAME \
#     $IMAGE_NAME .app/main.py

# Строка ниже выполнится ТОЛЬКО после того, как ты выйдешь из контейнера (exit)
echo "--- Вы вышли из контейнера, он был автоматически удален (благодаря --rm) ---"