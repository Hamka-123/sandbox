#!/bin/bash

# 1. Получаем абсолютный путь к папке, где лежит САМ этот скрипт
# SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# # 2. Переходим в эту папку, чтобы контекст сборки (точка) был правильным
# cd "$SCRIPT_DIR"

# cd "$(dirname "$0")"

docker run \
    --rm -it -d \
    --name alpine_container10 \
    --network NET_test_3 \
    -p 8000:8888 \
    alpine:v4.0.0