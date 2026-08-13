#!/bin/bash

echo "Шаг 4: Установка и настройка ISC DHCP Server..."

# 1. Установка
sudo apt update && sudo apt install -y isc-dhcp-server

# 2. Указываем интерфейс, на котором слушать (LAN)
# Правим файл /etc/default/isc-dhcp-server
sudo sed -i 's/INTERFACESv4=""/INTERFACESv4="LAN"/' /etc/default/isc-dhcp-server

# 3. Создаем конфигурацию подсети
sudo bash -c "cat > /etc/dhcp/dhcpd.conf << EOF
default-lease-time 600;
max-lease-time 7200;
authoritative;

subnet 192.168.60.0 netmask 255.255.255.0 {
  range 192.168.60.50 192.168.60.150;
  option routers 192.168.60.10;
  option domain-name-servers 8.8.8.8, 1.1.1.1;
}
EOF
"

# 4. Перезапуск
sudo systemctl restart isc-dhcp-server
sudo systemctl enable isc-dhcp-server

# Проверка статуса
if systemctl is-active --quiet isc-dhcp-server; then
    echo "✅ ISC DHCP Server успешно запущен на интерфейсе LAN."
else
    echo "❌ ОШИБКА: DHCP сервер не смог запуститься. Проверьте 'journalctl -u isc-dhcp-server'"
    exit 1
fi