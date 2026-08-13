#!/bin/bash

install_offline_packages() {
    [ -f "./server.conf" ] && source ./server.conf

    local TARGET_ROLE=$1 
    echo -e "${GREEN}>>> Установка пакетов для роли: $TARGET_ROLE...${NC}"
    
    local PKG_PATH="./packages"
    local START_DIR=$(pwd)

    if [ -d "$PKG_PATH" ]; then
        cd "$PKG_PATH" || return 1
        
        echo "Установка базовых компонентов (утилиты, ping, net-tools)..."
        #sudo dpkg -i --force-depends *iputils*.deb *net-tools*.deb > /dev/null 2>&1
        sudo dpkg -i --force-depends ./iputils-ping*.deb ./net-tools*.deb

        if [[ "$TARGET_ROLE" == "SERVER" ]]; then
            [[ $SELECTED_SERVICES == *"SSH"* ]] && echo "Установка SSH..." && sudo dpkg -i --force-depends *ssh*.deb > /dev/null 2>&1
            [[ $SELECTED_SERVICES == *"NAT"* ]] && echo "Установка nftables..." && sudo dpkg -i --force-depends *nftables*.deb > /dev/null 2>&1
            [[ $SELECTED_SERVICES == *"DHCP"* ]] && echo "Установка DHCP..." && sudo dpkg -i --force-depends *isc-dhcp-server*.deb > /dev/null 2>&1
            [[ $SELECTED_SERVICES == *"DNS"* ]] && echo "Установка DNS утилит..." && sudo dpkg -i --force-depends *dnsutils*.deb > /dev/null 2>&1
        else
            echo "Настройка клиента..."
            sudo dpkg -i --force-depends *openssh-client*.deb > /dev/null 2>&1
        fi
        
        sudo apt-get install -f -y > /dev/null 2>&1
        cd "$START_DIR"
    else
        echo -e "${YELLOW}Папка $PKG_PATH не найдена. Установка через репозитории...${NC}"
        local pkgs="iputils-ping net-tools openssh-client"
        if [[ "$TARGET_ROLE" == "SERVER" ]]; then
             [[ $SELECTED_SERVICES == *"SSH"* ]] && pkgs="$pkgs openssh-server"
             [[ $SELECTED_SERVICES == *"NAT"* ]] && pkgs="$pkgs nftables"
             [[ $SELECTED_SERVICES == *"DHCP"* ]] && pkgs="$pkgs isc-dhcp-server"
             [[ $SELECTED_SERVICES == *"DNS"* ]] && pkgs="$pkgs dnsutils"
        fi
        sudo apt-get update > /dev/null 2>&1
        sudo apt-get install -y $pkgs > /dev/null 2>&1
    fi
    echo -e "${GREEN}Установка завершена.${NC}"
}