#!/bin/bash
pwd #/Users/alinababenko/Documents/Israel_course/DevOps

#/Users/alinababenko/Documents/Israel_course/DevOps/docker_containers/alpine/Build_image.sh

# 1. Получаем абсолютный путь к папке, где лежит САМ этот скрипт
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# 2. Переходим в эту папку, чтобы контекст сборки (точка) был правильным
cd "$SCRIPT_DIR"

# 3. Теперь запускаем сборку
docker build \
    --pull --rm \
    -f Dockerfile \
    -t alpine:v4.0.0 \
    .
