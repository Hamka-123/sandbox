#!/bin/bash

# запустить на линукс машине с такой же ОС как и целевая а потом перенести папку с пакетами туда где собиаем iso

# Директория для пакетов
PKG_DIR="./packages"
mkdir -p $PKG_DIR
cd $PKG_DIR

# Список нужного софта
# openssh-server - удаленный доступ
# nftables - роутинг и NAT
# isc-dhcp-server - раздача IP
# bind9-dnsutils - команда 'host' для тестов
# net-tools, iputils-ping - базовые сетевые утилиты
PACKAGES="openssh-server nftables isc-dhcp-server bind9-dnsutils iputils-ping"

echo "=== Собираю список зависимостей ==="
# Получаем список всех зависимостей и самих пакетов
LIST=$(apt-cache depends --recurse --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances $PACKAGES | grep "^\w" | sort -u)

echo "=== Скачиваю пакеты ==="
apt-get download $LIST

echo "Готово! Теперь в папке $(pwd) лежат все .deb файлы."