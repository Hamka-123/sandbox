#!/bin/bash

apply_settings() {
    # Перечитываем конфиг, созданный в lib_init.sh
    if [ -f "./server.conf" ]; then
        source ./server.conf
    else
        echo -e "${RED}Ошибка: server.conf не найден!${NC}"
        return 1
    fi

    if [[ "$ROLE" == "SERVER" ]]; then
        setup_server
        # Принудительно обновляем интерфейсы
        sudo networkctl reload
        sudo networkctl reconfigure WAN
    else
        setup_client
        sudo networkctl reload
    fi
}

# --- СЕКЦИЯ СЕРВЕРА ---

setup_server() {
    echo -e "${GREEN}>>> Применение выбранных сервисов: $SELECTED_SERVICES${NC}"
    
    # 1. Сетевые интерфейсы (Netplan нужен всегда для роутера)
    generate_server_netplan

    # 2. SSH (если выбран)
    if [[ $SELECTED_SERVICES == *"SSH"* ]]; then
        echo "Настройка SSH..."
        sudo systemctl enable --now ssh
    fi
    
    # 3. Настройка Forwarding (если выбран NAT или DHCP)
    if [[ $SELECTED_SERVICES == *"NAT"* ]] || [[ $SELECTED_SERVICES == *"DHCP"* ]]; then
        echo "Включение IP Forwarding..."
        echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward > /dev/null
        sudo sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf
    fi
    
    # 4. Firewall & NAT из шаблона (если выбран)
    if [[ $SELECTED_SERVICES == *"NAT"* ]]; then
        setup_nftables_from_template
    fi
    
    # 5. DHCP Сервер (если выбран)
    if [[ $SELECTED_SERVICES == *"DHCP"* ]]; then
        setup_dhcp_server
    fi
    
    # 6. DNS Resolver (если выбран)
    if [[ $SELECTED_SERVICES == *"DNS"* ]]; then
        setup_dns_server
    fi
}

generate_server_netplan() {
    local YAML="/etc/netplan/01-netcfg.yaml"
    echo "Генерация Netplan (WAN/LAN)..."
    
    # Шапка с WAN
    sudo bash -c "cat > /tmp/net.yaml << EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    WAN:
      match: {macaddress: \"$WAN_MAC\"}
      set-name: WAN
      dhcp4: true
EOF"

    # Добавляем все LAN из конфига
    for (( i=1; i<=$LAN_COUNT; i++ )); do
        local MAC_VAR="LAN${i}_MAC"
        local IP_VAR="LAN${i}_IP"
        sudo bash -c "cat >> /tmp/net.yaml << EOF
    LAN$i:
      match: {macaddress: \"${!MAC_VAR}\"}
      set-name: LAN$i
      addresses: [${!IP_VAR}]
EOF"
    done
    
    sudo mv /tmp/net.yaml "$YAML"
    sudo chmod 600 "$YAML"
    sudo netplan apply
    sleep 2
}

setup_nftables_from_template() {
    local TEMPLATE="./nftables.template"
    local TARGET="/etc/nftables.conf"

    echo "Применение правил Firewall из шаблона..."
    if [ -f "$TEMPLATE" ]; then
        sudo cp "$TEMPLATE" "$TARGET"
        sudo nft -f "$TARGET"
        sudo systemctl enable --now nftables
        sudo systemctl restart nftables
    else
        echo -e "${RED}Ошибка: Шаблон $TEMPLATE не найден!${NC}"
    fi
}

setup_dhcp_server() {
    echo "Настройка DHCP (isc-dhcp-server)..."
    local DHCP_CONF="/etc/dhcp/dhcpd.conf"
    
    # Базовые настройки
    echo "authoritative;
default-lease-time 600;
max-lease-time 7200;" | sudo tee /tmp/dhcpd.conf > /dev/null

    # Генерация подсетей для всех LAN
    for (( i=1; i<=$LAN_COUNT; i++ )); do
        local IP_VAR="LAN${i}_IP"
        local ADDR=$(echo "${!IP_VAR}" | cut -d'/' -f1)
        local SUBNET=$(echo "$ADDR" | sed 's/\.[0-9]\+$/.0/')
        local PREFIX=$(echo "$ADDR" | sed 's/\.[0-9]\+$/./')
        
        echo "subnet $SUBNET netmask 255.255.255.0 {
  range ${PREFIX}100 ${PREFIX}200;
  option routers $ADDR;
  option domain-name-servers $ADDR, 8.8.8.8;
}" | sudo tee -a /tmp/dhcpd.conf > /dev/null
    done
    
    sudo mv /tmp/dhcpd.conf "$DHCP_CONF"

    # Привязка к интерфейсам
    local LAN_IF_LIST=""
    for (( i=1; i<=$LAN_COUNT; i++ )); do LAN_IF_LIST+="LAN$i "; done
    sudo sed -i "s/INTERFACESv4=\"\"/INTERFACESv4=\"$LAN_IF_LIST\"/" /etc/default/isc-dhcp-server
    
    sudo systemctl restart isc-dhcp-server
}

setup_dns_server() {
    echo "Настройка DNS (resolved)..."
    local RESOLVED_CONF="/etc/systemd/resolved.conf"
    
    # Очистка старых доп. адресов прослушивания
    sudo sed -i '/^DNSStubListenerExtra=/d' "$RESOLVED_CONF"
    
    # Добавляем IP всех LAN интерфейсов в прослушку
    local ALL_IPS=$(hostname -I)
    for IP in $ALL_IPS; do
        if [[ $IP != "127.0.0.1" ]]; then
            sudo sed -i "/\[Resolve\]/a DNSStubListenerExtra=$IP" "$RESOLVED_CONF"
        fi
    done
    
    sudo systemctl restart systemd-resolved
}

# --- СЕКЦИЯ КЛИЕНТА ---

setup_client() {
    echo -e "${GREEN}>>> Настройка роли: КЛИЕНТ${NC}"
    local YAML="/etc/netplan/01-netcfg.yaml"
    
    if [[ "$MODE" == "DHCP" ]]; then
        sudo bash -c "cat > /tmp/client_net.yaml << EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    LAN:
      match: {macaddress: \"$CLIENT_MAC\"}
      set-name: LAN
      dhcp4: true
EOF"
    else
        local CLEAN_GW=$(echo "$GW" | cut -d'/' -f1)
        sudo bash -c "cat > /tmp/client_net.yaml << EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    LAN:
      match: {macaddress: \"$CLIENT_MAC\"}
      set-name: LAN
      addresses: [$IP]
      routes:
        - to: default
          via: $CLEAN_GW
      nameservers:
        addresses: [$CLEAN_GW, 8.8.8.8]
EOF"
    fi
    
    sudo mv /tmp/client_net.yaml "$YAML"
    sudo chmod 600 "$YAML"
    sudo netplan apply
}