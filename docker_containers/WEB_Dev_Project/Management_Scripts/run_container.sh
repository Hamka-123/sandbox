#!/bin/bash

# Переменные
IMAGE_NAME="python_server_1"
IMAGE_VERSION="1.0.0"
CONTAINER_NAME="${IMAGE_NAME}_1"

# Определяем путь к директории проекта (аналог $PSScriptRoot)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_FOLDER="$(cd "${SCRIPT_DIR}/../Python_Server_Image" && pwd)"

# Массив аргументов
DOCKER_ARGUMENTS=(
    "run"
    "--detach"
    "--interactive"
    "--rm"
    "--name" "${CONTAINER_NAME}"
    "--publish" "8002:8000"
    "--mount" "type=bind,source=${PROJECT_FOLDER}/http_root,target=/http_root"
    "${IMAGE_NAME}:${IMAGE_VERSION}"
)

# Вывод команды желтым цветом
echo -e "\e[33m${DOCKER_ARGUMENTS[*]}\e[0m"

# Запуск Docker
docker "${DOCKER_ARGUMENTS[@]}"