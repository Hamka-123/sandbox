#!/bin/bash

generate_final_report() {
    local REPORT="machine_report.txt"
    local CYAN='\033[0;36m'
    local YELLOW='\033[1;33m'
    local GREEN='\033[0;32m'
    local RED='\033[0;31m'
    local NC='\033[0m'

    echo -e "${GREEN}>>> Шаг 4: Ожидание стабилизации сети и генерация отчета...${NC}"
    sleep 5

    print_header() {
        local text="$1"
        echo -e "\n${CYAN}${text}${NC}"
    }

    {
        echo "====================================================="
        echo "      DEV OPS CONFIGURATION REPORT (v2)"
        echo "      Дата: $(date)"
        echo "      Роль системы: $ROLE"
        echo "====================================================="

        print_header "[1] ОБЩАЯ ИНФОРМАЦИЯ"
        hostnamectl | grep -E "Static hostname|Operating System|Kernel" || echo "Hostname: $(hostname)"
        echo "Uptime: $(uptime -p)"

        print_header "[2] СЕТЕВЫЕ ИНТЕРФЕЙСЫ"
        echo "---------------------------------------------------------------------------------------"
       
        printf "%-12s %-8s %-18s %-30s %-18s\n" "INTERFACE" "STATUS" "IPv4" "IPv6" "MAC_ADDRESS"
        echo "---------------------------------------------------------------------------------------"
        
        ip -br link show | awk '{print $1, $2, $3}' | while read -r IFACE STATUS MAC; do
            # Очищаем статус от лишних скобок, если есть
            STATUS_CLEAN=$(echo $STATUS | tr -d '[]')
            
            IPV4=$(ip -f inet -br addr show "$IFACE" 2>/dev/null | awk '{print $3}' | head -n 1)
            [ -z "$IPV4" ] && IPV4="-"
            
            IPV6=$(ip -f inet6 -br addr show "$IFACE" 2>/dev/null | awk '{print $3}' | head -n 1)
            [ -z "$IPV6" ] && IPV6="-"
            
            # Форматированный вывод без использования внешней утилиты column
            printf "%-12s %-8s %-18s %-30s %-18s\n" "$IFACE" "$STATUS_CLEAN" "$IPV4" "$IPV6" "$MAC"
        done
        echo "---------------------------------------------------------------------------------------"

        print_header "[3] СТАТУС КРИТИЧЕСКИХ СЕРВИСОВ"
        check_svc() {
            local label=$1
            local svc=$2
            if systemctl is-active --quiet "$svc"; then
                echo -e "$label ($svc): ${GREEN}RUNNING${NC}"
            else
                echo -e "$label ($svc): ${RED}FAILED/STOPPED${NC}"
            fi
        }
        check_svc "SSH Access" "ssh"
        check_svc "DNS Resolver" "systemd-resolved"
        if [[ "$ROLE" == "SERVER" ]]; then
            check_svc "DHCP Server" "isc-dhcp-server"
            check_svc "NAT/Firewall" "nftables"
            check_svc "Router (Forwarding)" "systemd-networkd"
        fi

        print_header "[4] ПРОВЕРКА СВЯЗНОСТИ (Connectivity)"
        if [[ "$ROLE" == "CLIENT" ]]; then
            # 1. Пытаемся взять шлюз из переменной, если она есть
            local CLEAN_GW=$(echo "$GW" | cut -d'/' -f1)

            # 2. Если переменная пуста (как в случае с DHCP), ищем шлюз в системе
            if [ -z "$CLEAN_GW" ]; then
                CLEAN_GW=$(ip route show default | awk '/default/ {print $3}' | head -n 1)
            fi

            # 3. Если всё еще пусто — значит шлюз реально не получен
            if [ -z "$CLEAN_GW" ]; then
                CLEAN_GW="Gateway Not Set"
                echo -e "Пинг шлюза: ${RED}ОШИБКА (Шлюз не найден)${NC}"
            else
                echo -n "Пинг шлюза ($CLEAN_GW): "
                ping -c 2 -W 2 "$CLEAN_GW" > /dev/null 2>&1 && echo -e "${GREEN}OK${NC}" || echo -e "${RED}FAIL${NC}"
            fi
        fi
        echo -n "Пинг интернета (8.8.8.8): "
        ping -c 2 -W 2 8.8.8.8 > /dev/null 2>&1 && echo -e "${GREEN}OK${NC}" || echo -e "${RED}FAIL${NC}"

        print_header "[5] ПРОВЕРКА DNS"
        echo -n "Резолвинг google.com: "
        host google.com > /dev/null 2>&1 && echo -e "${GREEN}OK${NC}" || echo -e "${RED}FAIL${NC}"

        if [[ "$ROLE" == "SERVER" ]]; then
            print_header "[6] КОНФИГУРАЦИЯ NAT (nftables)"
            echo "-----------------------------------------------------"
            sudo nft list table ip nat 2>/dev/null || echo "NAT table not found"
            echo "-----------------------------------------------------"
            echo -e "IP Forwarding: $([[ $(cat /proc/sys/net/ipv4/ip_forward 2>/dev/null) == "1" ]] && echo -e "${GREEN}ENABLED${NC}" || echo -e "${RED}DISABLED${NC}")"

            print_header "[7] СПИСОК DHCP КЛИЕНТОВ (Leases)"
            echo "---------------------------------------------------------------------------------------"
            LEASES_FILE="/var/lib/dhcp/dhcpd.leases"
            if [ -f "$LEASES_FILE" ] && grep -q "^lease" "$LEASES_FILE"; then
                printf "${YELLOW}%-16s %-20s %-20s %s${NC}\n" "IP_ADDRESS" "MAC_ADDRESS" "HOSTNAME" "STATUS"
                awk '/^lease/ { ip=$2 } /hardware ethernet/ { mac=$3; gsub(/;/,"",mac) } /client-hostname/ { name=$2; gsub(/[";]/,"",name) } /^}/ { printf "%s|%s|%s\n", ip, mac, (name ? name : "unknown"); ip=mac=name="" }' "$LEASES_FILE" | sort -u | while IFS='|' read -r IP MAC HOSTNAME; do
                    ping -c 1 -W 1 "$IP" > /dev/null 2>&1 && ST="${GREEN}ONLINE${NC}" || ST="${RED}OFFLINE${NC}"
                    printf "%-16s %-20s %-20s %b\n" "$IP" "$MAC" "$HOSTNAME" "$ST"
                done
            else
                echo "Активных аренд (leases) пока нет."
            fi
            echo "---------------------------------------------------------------------------------------"
        fi

        print_header "[8] РЕСУРСЫ"
        MEM_TOTAL=$(free -m | awk '/Mem:/ {print $2}')
        MEM_USED=$(free -m | awk '/Mem:/ {print $3}')
        MEM_PCT=$(( 100 * MEM_USED / MEM_TOTAL ))
        echo -e "Память: $(free -h | awk '/Mem:/ {print $3 "/" $2}') (${YELLOW}$MEM_PCT%${NC})"
        echo -e "Диск:   $(df -h / | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}')"

    } | tee "$REPORT"

    # Очистка файла от ANSI-кодов
    sed -i 's/\x1b\[[0-9;]*m//g' "$REPORT"

    echo -e "\n${GREEN}Отчет сохранен в файл: $(pwd)/$REPORT${NC}"
}

# --- Блок прямого запуска ---
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    [ -f "./server.conf" ] && source ./server.conf
    ROLE=${ROLE:-"SERVER"}
    generate_final_report
fi