#!/bin/bash

# 1. Установка
sudo apt-get update && sudo apt-get install -y nftables

# Путь к файлу правил относительно текущей папки
RULES_FILE="./gateway.nft"

echo "Начинаю настройку роутинга и NAT..."

# 1. Включаем IP Forwarding в ядре
echo "Включаю IP Forwarding..."
sudo sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf
sudo sysctl -p

# 2. Проверяем наличие файла правил
if [ ! -f "$RULES_FILE" ]; then
    echo "❌ ОШИБКА: Файл $RULES_FILE не найден!"
    exit 1
fi

# 3. Применяем правила nftables
echo "Применяю правила nftables..."
if sudo nft -f "$RULES_FILE"; then
    # Копируем в системный конфиг для автозагрузки
    sudo cp "$RULES_FILE" /etc/nftables.conf
    sudo systemctl enable nftables
    sudo systemctl restart nftables
    echo "✅ Роутинг и NAT настроены успешно."
else
    echo "❌ ОШИБКА: Не удалось применить правила nftables. Проверьте синтаксис."
    exit 1
fi