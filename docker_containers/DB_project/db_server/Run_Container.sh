#!/bin/bash

# Название контейнера и образа
CONTAINER_NAME="db_server_v2.0"
IMAGE_NAME="xampp_mariadb:v2.0"

# 0. Проверяем, не запущен ли уже контейнер с таким именем, и удаляем его
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "--- Удаляем старый контейнер $CONTAINER_NAME ---"
    docker rm -f $CONTAINER_NAME
fi

# 1. Создаем том для базы (если его нет, Docker сделает это сам, но можно и вручную)
# Проверяем, существует ли том. Если нет (-z проверяет пустую строку) — создаем.
# if [ -z "$(docker volume ls -q -f name=^mysql$)" ]; then
#     echo "--- Создаем том mysql ---"
#     docker volume create mysql
# else
#     echo "--- Том mysql уже существует, пропускаем ---"
# fi

# 2. Запуск контейнера
echo "--- Запуск контейнера $CONTAINER_NAME ---"
docker run -d \
    --name $CONTAINER_NAME \
    --platform linux/amd64 \
    -p 80:80 \
    -p 443:443 \
    -p 3306:3306 \
    --mount type=volume,source=www2,target=/opt/lampp/htdocs \
    --mount type=volume,source=mysql2,target=/opt/lampp/var/mysql \
    $IMAGE_NAME

echo "--- Контейнер запущен! ---"
echo "Web: http://localhost:80"
echo "PHP MyAdmin http://localhost:80/phpmyadmin"
echo "DB Port: 3308"
