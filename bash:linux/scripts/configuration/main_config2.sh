#!/bin/bash 

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 0 - Пути и права
cd "$(dirname "$0")" || exit
chmod +x ./*.sh

echo -e "${GREEN}=== Запуск настройки сервера BUBBLE ===${NC}"

# 1 - Hostname
HOST_NAME="bubble"
sudo bash ./rename_host.sh "$HOST_NAME" > /dev/null
[[ "$(hostname)" == "$HOST_NAME" ]] && echo -e "1. Hostname: ${GREEN}OK ($HOST_NAME)${NC}" || echo -e "1. Hostname: ${RED}FAIL${NC}"

# 2 - Network
WAN_MAC="00:0C:29:36:7A:12"
LAN_MAC="00:0C:29:36:7A:1C"
LAN_IP_ADDRESS="192.168.60.10/24"
bash ./change_network_config.sh "$WAN_MAC" "$LAN_MAC" "$LAN_IP_ADDRESS" > /dev/null
sleep 1

# Короткая проверка сети
LAN_IP=$(ip -4 addr show LAN 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
if [[ "$LAN_IP" == "192.168.60.10" ]]; then
    echo -e "2. Network LAN: ${GREEN}OK (192.168.60.10)${NC}"
else
    echo -e "2. Network LAN: ${RED}FAIL (Check interfaces)${NC}"
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
if host google.com > /dev/null 2>&1; then DNS_RES="OK"; else DNS_RES="FAIL"; fi

if [ "$DNS_RULES" -gt 0 ]; then
    echo -e "5. DNS Rules: ${GREEN}OK ($DNS_RULES rules)${NC}"
    echo -e "6. Internet Access: ${GREEN}$DNS_RES${NC}"
else
    echo -e "5. DNS Rules: ${RED}MISSING${NC}"
fi

echo -e "${GREEN}=== Настройка завершена ===${NC}"