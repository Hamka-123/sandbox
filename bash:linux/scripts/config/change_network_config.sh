#!/bin/bash

# Константы из аргументов
WAN_MAC="$1"
LAN1_MAC="$2"
LAN2_MAC="$3"
LAN1_ADDRESS="$4"
LAN2_ADDRESS="$5"

# Имена интерфейсов, которые мы хотим закрепить
LAN1_NAME="LAN1"
LAN2_NAME="LAN2"
WAN_NAME="WAN"

NETPLAN_PATH=""
CONFIG_FILE="$NETPLAN_PATH/50-cloud-init.yaml" # Имя по умолчанию, можно изменить

echo "Начинаю настройку Netplan..."

# 1. Бэкапим старые конфиги, чтобы не было конфликтов
sudo mkdir -p $NETPLAN_PATH/backup
for file in $NETPLAN_PATH/*.yaml; do
    if [[ -f "$file" ]]; then
        sudo mv "$file" "$NETPLAN_PATH/backup/$(basename "$file").old"
        echo "Старый конфиг $file перемещен в backup."
    fi
done

# 2. Создаем новый YAML конфиг
# Мы используем match по MAC-адресу и сразу переименовываем (set-name)
sudo bash -c "cat > $CONFIG_FILE << EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    $WAN_NAME:
      match:
        macaddress: \"$WAN_MAC\"
      set-name: $WAN_NAME
      dhcp4: true
    $LAN1_NAME:
      match:
        macaddress: \"$LAN1_MAC\"
      set-name: $LAN1_NAME
      addresses:
        - $LAN1_ADDRESS
    $LAN2_NAME:
      match:
        macaddress: \"$LAN2_MAC\"
      set-name: $LAN2_NAME
      addresses:
        - $LAN2_ADDRESS
EOF
"

echo "Новый конфиг $CONFIG_FILE создан."

# 3. Устанавливаем права (ОБЯЗАТЕЛЬНО до применения)
sudo chmod 600 "$CONFIG_FILE"
echo "Права доступа ограничены (600)."

# 4. Применяем настройки
echo "Проверка и применение настроек..."
sudo netplan apply

echo "Готово! Интерфейсы переименованы в $WAN_NAME и $LAN1_NAME и $LAN2_NAME."