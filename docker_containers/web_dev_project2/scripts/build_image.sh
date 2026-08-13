#!/bin/bash

# Определение переменных
IMAGE_NAME="python_server_1"
IMAGE_VERSION="1.0.0"

# Получаем путь к директории скрипта (аналог $PSScriptRoot)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_FOLDER="$(cd "${SCRIPT_DIR}/../python_server" && pwd)"
DOCKER_FILE="${PROJECT_FOLDER}/Dockerfile"

# Массив аргументов для Docker
DOCKER_ARGUMENTS=(
    "build"
    "--rm"
    "-f" "${DOCKER_FILE}"
    "-t" "${IMAGE_NAME}:${IMAGE_VERSION}"
    "${PROJECT_FOLDER}"
)

# Вывод команды желтым цветом (используя ANSI-коды)
# \e[33m - желтый, \e[0m - сброс цвета
echo -e "\e[33m${DOCKER_ARGUMENTS[*]}\e[0m"

# Запуск Docker с развертыванием массива аргументов
docker "${DOCKER_ARGUMENTS[@]}"