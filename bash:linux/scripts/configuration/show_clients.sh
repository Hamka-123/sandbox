#!/bin/bash

LEASES_FILE="/var/lib/dhcp/dhcpd.leases"

echo -e "\n--- Текущие клиенты в сети LAN ---"
printf "%-15s | %-17s | %-20s\n" "IP Address" "MAC Address" "Hostname"
echo "------------------------------------------------------------"

# Парсим файл: ищем строки с 'lease', 'hardware' и 'client-hostname'
awk '
    /lease / { ip=$2 }
    /hardware ethernet/ { mac=$3; gsub(/;/, "", mac) }
    /client-hostname/ { name=$2; gsub(/[";]/, "", name); 
        printf "%-15s | %-17s | %-20s\n", ip, mac, name 
    }
' "$LEASES_FILE" | sort -u
echo -e "------------------------------------------------------------\n"