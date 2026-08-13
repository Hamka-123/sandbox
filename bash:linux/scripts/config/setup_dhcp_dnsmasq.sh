#!/bin/bash

echo "Шаг 4: Установка и настройка DHCP/DNS (dnsmasq)..."

# 1. Установка
sudo apt-get update && sudo apt-get install -y dnsmasq

# 2. Бэкап старого конфига
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.bak

# 3. Создаем новый конфиг
# Интерфейс: LAN
# Диапазон: 192.168.60.50 - 192.168.60.150
# Аренда: 12 часов
sudo bash -c "cat > /etc/dnsmasq.conf << EOF
interface=LAN
dhcp-range=192.168.60.50,192.168.60.150,12h
dhcp-option=option:router,192.168.60.10
dhcp-option=option:dns-server,1.1.1.1,8.8.8.8
bind-interfaces
EOF
"

# 4. Перезапуск
sudo systemctl restart dnsmasq
sudo systemctl enable dnsmasq

echo "✅ DHCP сервер запущен на интерфейсе LAN."