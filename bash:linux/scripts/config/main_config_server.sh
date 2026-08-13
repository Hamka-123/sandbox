#!/bin/bash 

# 0 - Исправляем проблему путей
# Переходим в папку, где лежит сам основной скрипт
cd "$(dirname "$0")" || exit

chmod +x ./* # Делаем все скрипты в текущей папке исполняемыми автоматически

# 1 - change host name
HOST_NAME="bubble"
echo "---------------Запускаю переименование в $HOST_NAME"
sudo bash ./rename_host.sh "$HOST_NAME"
 # tests
hostnamectl

# 2 - setup network interfaces netpaln
WAN_MAC="00:0C:29:36:7A:12"
LAN_MAC="00:0C:29:36:7A:1C"
LAN_IP_ADDRESS="192.168.60.10/24"

echo "---------------Запускаю настройку сетевых интерфейсов"
bash ./change_network_config.sh "$WAN_MAC" "$LAN_MAC" "$LAN_IP_ADDRESS"

  # tests
echo "Ожидание инициализации интерфейсов..."
sleep 2 # Даем системе пару секунд "прожевать" настройки

check_interface() {
    local iface=$1
    # Проверяем, существует ли интерфейс
    if ! ip link show "$iface" > /dev/null 2>&1; then
        echo "❌ ОШИБКА: Интерфейс $iface не найден в системе!"
        return 1
    fi

    # Проверяем, поднят ли он (UP)
    if [[ ! $(ip link show "$iface") == *"state UP"* ]]; then
        echo "⚠️ ПРЕДУПРЕЖДЕНИЕ: Интерфейс $iface существует, но он DOWN (проверьте кабель/линк)."
    fi

    # Проверяем наличие IP
    local ip_addr=$(ip -4 addr show "$iface" | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
    if [ -z "$ip_addr" ]; then
        echo "❌ ОШИБКА: Интерфейс $iface не получил IP-адрес!"
        return 1
    else
        echo "✅ Интерфейс $iface готов. IP: $ip_addr"
        return 0
    fi
}

echo "--- Результаты проверки сети ---"
check_interface "WAN" || exit 1
check_interface "LAN" || exit 1


# 3 - setup routing
echo "---------------Запускаю настройку маршрутизации..."
bash ./setup_routing.sh
 # tests
sudo nft list ruleset
sudo nft list chain ip nat postrouting
#if ping -I LAN -c 2 8.8.8.8 > /dev/null 2>&1; then
#    echo "🌐 Интернет в локальной сети доступен!"
#else
#    echo "⚠️ Внимание: Пинг через LAN не прошел. Проверьте настройки WAN."
#fi

# 4 - setup DHCP
echo "---------------Запускаю настройку DHCP..."
bash ./setup_dhcp_classic.sh
# Посмотреть, кто получил IP-адреса
#cat /var/lib/dhcp/dhcpd.leases
bash ./show_clients.sh
# 5 - setup DNS
# добавила в gateway.nft в chain input
#  # Разрешаем DNS только со стороны локальной сети
       # iifname "LAN" udp dport 53 accept
       # iifname "LAN" tcp dport 53 accept
# (Firewall rules test)
echo "--------------- Проверка DNS (Firewall)"

# 1. Проверяем, есть ли правила для 53 порта в nftables
DNS_RULES=$(sudo nft list ruleset | grep -c "dport 53")

# 2. Пробуем сделать резолв (только если на сервере настроен интернет)
if host google.com > /dev/null 2>&1; then
    DNS_RESOLVE="OK"
else
    DNS_RESOLVE="FAIL"
fi

if [ "$DNS_RULES" -gt 0 ]; then
    echo "✅ DNS Ports (53): OPEN ($DNS_RULES rules)"
    echo "✅ DNS Resolution: $DNS_RESOLVE"
else
    echo "❌ DNS Ports (53): CLOSED"
fi
