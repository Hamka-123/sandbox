#!/bin/bash

choose_role() {
    # Выбор роли
    ROLE_CHOICE=$(whiptail --title "Мастер настройки" --menu "Выберите роль системы:" 15 60 2 \
    "1" "СЕРВЕР (Router, NAT, DHCP, DNS)" \
    "2" "КЛИЕНТ (Рабочая станция)" 3>&1 1>&2 2>&3)

    [ $? -ne 0 ] && exit 1

    if [[ "$ROLE_CHOICE" == "1" ]]; then
        ROLE="SERVER"
        # Выбор сервисов галочками
        SERVICES=$(whiptail --title "Компоненты сервера" --checklist \
        "Выберите сервисы (Пробел - выбор):" 20 60 10 \
        "SSH" "Удаленный доступ" ON \
        "NAT" "Маршрутизация и Интернет" ON \
        "DHCP" "Раздача IP адресов" ON \
        "DNS" "Локальный резолвер" ON 3>&1 1>&2 2>&3)
        SELECTED_SERVICES=$(echo $SERVICES | sed 's/"//g')
    else
        ROLE="CLIENT"
    fi
}

generate_config() {
    CONF="server.conf"
    echo "# Конфигурация от $(date)" > "$CONF"
    echo "ROLE=\"$ROLE\"" >> "$CONF"
    [ -n "$SELECTED_SERVICES" ] && echo "SELECTED_SERVICES=\"$SELECTED_SERVICES\"" >> "$CONF"

    # Сбор всех интерфейсов
    mapfile -t IFACES < <(ls /sys/class/net | grep -v "lo")
    IFACE_MENU=()
    for IF in "${IFACES[@]}"; do
        MAC=$(cat "/sys/class/net/$IF/address")
        IFACE_MENU+=("$IF" "MAC: $MAC")
    done

    if [[ "$ROLE" == "SERVER" ]]; then
        # Назначение WAN
        WAN_IF=$(whiptail --title "Настройка WAN" --menu \
        "Выберите интерфейс для ВНЕШНЕЙ сети (Internet):" 20 60 10 \
        "${IFACE_MENU[@]}" 3>&1 1>&2 2>&3)
        
        WAN_MAC=$(cat "/sys/class/net/$WAN_IF/address")
        echo "WAN_IF=\"$WAN_IF\"" >> "$CONF"
        echo "WAN_MAC=\"$WAN_MAC\"" >> "$CONF"

        # Назначение LAN
        LAN_COUNT=0
        for IF in "${IFACES[@]}"; do
            [[ "$IF" == "$WAN_IF" ]] && continue
            
            if whiptail --title "Настройка LAN" --yesno "Использовать $IF как LAN?" 10 60; then
                ((LAN_COUNT++))
                L_MAC=$(cat "/sys/class/net/$IF/address")
                L_IP=$(whiptail --title "IP для LAN$LAN_COUNT" --inputbox \
                "Введите IP/MASK для $IF:" 10 60 "192.168.$((10+LAN_COUNT)).1/24" 3>&1 1>&2 2>&3)
                
                echo "LAN${LAN_COUNT}_ORIG_IF=\"$IF\"" >> "$CONF"
                echo "LAN${LAN_COUNT}_MAC=\"$L_MAC\"" >> "$CONF"
                echo "LAN${LAN_COUNT}_IP=\"$L_IP\"" >> "$CONF"
            fi
        done
        echo "LAN_COUNT=$LAN_COUNT" >> "$CONF"
    else
        # Настройка Клиента
        CLIENT_IF=$(whiptail --title "Интерфейс клиента" --menu "Выберите карту:" 20 60 10 "${IFACE_MENU[@]}" 3>&1 1>&2 2>&3)
        echo "CLIENT_MAC=\"$(cat /sys/class/net/$CLIENT_IF/address)\"" >> "$CONF"
        
        MODE=$(whiptail --title "Режим" --menu "Настройка IP:" 15 60 2 "DHCP" "Авто" "STATIC" "Вручную" 3>&1 1>&2 2>&3)
        echo "MODE=\"$MODE\"" >> "$CONF"
        if [[ "$MODE" == "STATIC" ]]; then
            echo "IP=\"$(whiptail --inputbox "IP/MASK:" 10 60 3>&1 1>&2 2>&3)\"" >> "$CONF"
            echo "GW=\"$(whiptail --inputbox "Шлюз (IP сервера):" 10 60 3>&1 1>&2 2>&3)\"" >> "$CONF"
        fi
    fi
}