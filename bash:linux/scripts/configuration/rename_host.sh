#!/bin/bash

# 1. Защита от пустых аргументов
if [ -z "$1" ]; then
    echo "Ошибка: не указано новое имя хоста"
    exit 1
fi

readonly NEW_HOSTNAME="${1,,}" # ,, переводит в нижний регистр (bash 4.0+)
CURRENT_HOSTNAME="$(hostname)"
CURRENT_HOSTNAME="${CURRENT_HOSTNAME,,}"

echo "Текущее имя: $CURRENT_HOSTNAME"
echo "Целевое имя: $NEW_HOSTNAME"

if [[ "$CURRENT_HOSTNAME" != "$NEW_HOSTNAME" ]]; then 
    echo "Изменяю имя хоста на $NEW_HOSTNAME..."
    sudo hostnamectl set-hostname "$NEW_HOSTNAME"
    
    # Рекомендуется также обновить /etc/hosts, чтобы sudo не тормозило
    sudo sed -i "s/127.0.1.1.*/127.0.1.1\t$NEW_HOSTNAME/" /etc/hosts
else
    echo "Имена совпадают. Ничего не меняю (Do nothing)."
fi