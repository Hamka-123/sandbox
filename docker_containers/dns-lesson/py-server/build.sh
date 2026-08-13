#!/bin/bash

# Используем относительные пути, чтобы скрипт работал у любого коллеги
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
IMAGE_NAME="py-server"
# Автоматическая версия (например, дата и время)
IMAGE_TAG=$(date +%Y%m%d-%H%M)

docker build \
--rm \
-f "$SCRIPT_DIR/Dockerfile" \
-t "$IMAGE_NAME:$IMAGE_TAG" \
-t "$IMAGE_NAME:latest" \
"$SCRIPT_DIR"