#!/bin/bash 

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 0 - Пути и права
cd "$(dirname "$0")" || exit
chmod +x ./*.sh

# Подключаем конфиг
source ./server.conf

echo -e "${GREEN}=== Запуск настройки сервера $(hostname) ===${NC}"

# 1 - Hostname
#echo -n "Введите новое имя сервера (нажмите Enter, чтобы оставить '$(hostname)'): "
#read -r INPUT_NAME

# Если ввод пустой, используем значение по умолчанию
#HOST_NAME=${INPUT_NAME:-"$(hostname)"}

#echo "Настраиваю имя: $HOST_NAME..."
#sudo bash ./rename_host.sh "$HOST_NAME" > /dev/null

# Тест
#[[ "$(hostname)" == "$HOST_NAME" ]] && echo -e "1. Hostname: ${GREEN}OK ($HOST_NAME)${NC}" || echo -e "1. Hostname: ${RED}FAIL${NC}"

# 2 - Network
# Динамически берем MAC на основе имен из конфига
WAN_MAC="$WAN_MAC"
LAN1_MAC="$LAN1_MAC"
LAN2_MAC="$LAN2_MAC"
LAN1_IP_ADDRESS="$LAN1_IP"
LAN2_IP_ADDRESS="$LAN2_IP"

bash ./change_network_config.sh "$WAN_MAC" "$LAN1_MAC" "$LAN2_MAC" "$LAN1_IP_ADDRESS" "$LAN2_IP_ADDRESS" > /dev/null
sleep 1

# Короткая проверка сети
LAN_IP=$(ip -4 addr show LAN2 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
if [[ "$LAN_IP" == "$LAN1_IP" ]]; then
    echo -e "2. Network LAN1: ${GREEN}OK ($LAN1_IP)${NC}"
else
    echo -e "2. Network LAN1: ${RED}FAIL (Check interfaces)${NC}"
fi

# 3 - Routing & NAT
bash ./setup_routing.sh > /dev/null
FW_ON=$(cat /proc/sys/net/ipv4/ip_forward)
NAT_OK=$(sudo nft list table ip nat 2>/dev/null | grep -c "masquerade")
if [[ "$FW_ON" == "1" && "$NAT_OK" -gt 0 ]]; then
    echo -e "3. Routing & NAT: ${GREEN}OK${NC}"
else
    echo -e "3. Routing: ${RED}FAIL${NC}"
fi

# 4 - DHCP
bash ./setup_dhcp_classic.sh > /dev/null
if systemctl is-active --quiet isc-dhcp-server; then
    echo -e "4. DHCP Server: ${GREEN}OK${NC}"
    bash ./show_clients.sh
else
    echo -e "4. DHCP Server: ${RED}FAIL${NC}"
fi

# 5 - DNS
DNS_RULES=$(sudo nft list ruleset 2>/dev/null | grep -c "dport 53")

bash ./dns_to_server.sh "$NET"
if host google.com > /dev/null 2>&1; then DNS_RES="OK"; else DNS_RES="FAIL"; fi

if [ "$DNS_RULES" -gt 0 ]; then
    echo -e "5. DNS Rules: ${GREEN}OK ($DNS_RULES rules)${NC}"
    echo -e "6. Internet Access: ${GREEN}$DNS_RES${NC}"
else
    echo -e "5. DNS Rules: ${RED}MISSING${NC}"
fi

echo -e "${GREEN}=== Настройка завершена ===${NC}"