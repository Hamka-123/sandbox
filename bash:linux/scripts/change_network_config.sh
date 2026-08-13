#!/bin/bash 

#constants
LAN_MAC="00:0c:29:47:84:b4"
WAN_MAC="00:0c:29:47:84:aa"

LAN_INTERFACE="LAN"
WAN_INTERFACE="WAN"

LAN_ADDRESS="192.168.60.10/24"

NET_PATH="/etc/systemd/network"
LAN_NET_CONFIG_FILE="$NET_PATH/20-$LAN_INTERFACE.network"
WAN_NET_CONFIG_FILE="$NET_PATH/20-$WAN_INTERFACE.network"
LAN_LINK_CONFIG_FILE="$NET_PATH/10-$LAN_INTERFACE.link"
WAN_LINK_CONFIG_FILE="$NET_PATH/10-$WAN_INTERFACE.link"

# Перебираем все файлы в директории
for file in /etc/systemd/network/*; do
    
    # 1. Проверяем, что это обычный файл (не папка)
    # 2. Проверяем, что имя файла НЕ заканчивается на .old
    if [[ -f "$file" && ! "$file" == *.old ]]; then
        sudo mv "$file" "${file}.old" && echo "Отключен: $file"
    else
        echo "Пропуск: $file (уже отключен или не является файлом)"
    fi
done

#LAN
sudo bash -c "cat > $LAN_LINK_CONFIG_FILE << EOF
[Match]
MACAddress=$LAN_MAC

[Link]
Name=$LAN_INTERFACE
EOF
"
echo "Конфигурация для $LAN_INTERFACE создана."

#WAN
sudo bash -c "cat > $WAN_LINK_CONFIG_FILE << EOF
[Match]
MACAddress=$WAN_MAC

[Link]
Name=$WAN_INTERFACE
EOF
"
echo "Конфигурация для $WAN_INTERFACE создана."


sudo bash -c "cat > $LAN_NET_CONFIG_FILE << EOF
[Match]
MACAddress=$LAN_MAC

[Network]
Address=$LAN_ADDRESS

EOF
"
sudo bash -c "cat > $WAN_NET_CONFIG_FILE << EOF
[Match]
MACAddress=$WAN_MAC

[Network]
DHCP=yes

EOF
"

# Persist
sudo systemctl restart systemd-networkd