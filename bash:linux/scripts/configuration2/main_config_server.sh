#!/bin/bash 

# 1 - change host name
HOST_NAME="Hamka_test"
echo "Запускаю переименование в $HOST_NAME"
bash ./rename_host.sh "$HOST_NAME"

# 2 - setup network interfaces netpaln
  
WAN_MAC="00:0C:29:36:7A:12"
LAN_MAC="00:0C:29:36:7A:1C"
LAN_IP_ADDRESS="192.168.60.10/24"

bash ./change_network_config.sh "$WAN_MAC" "$LAN_MAC" "$LAN_IP_ADDRESS"

  # tests
if [ $? -eq 0 ]; then
    echo "Сеть настроена успешно."
else
    echo "Ошибка при настройке сети!"
    exit 1
fi


# 3 - setup routing
    # enable ip forwarding /etc/sysctl.conf
    #sudo sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf

    # write rules to nftables
    # restart service 
    # tests

# 4 - setup DHCP

# 5 - setup DNS