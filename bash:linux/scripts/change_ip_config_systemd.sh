#!/bin/bash
# Constants
LAN_MAC="00:0c:29:1c:ce:e9"
WAN_MAC="00:50:56:37:87:14"
LAN_INTERFACE="LAN"
WAN_INTERFACE="WAN"

LAN_NET_CONFIG_FILE="/etc/systemd/network/20-$LAN_INTERFACE.network"
WAN_NET_CONFIG_FILE="/etc/systemd/network/20-$WAN_INTERFACE.network"
LAN_LINK_CONFIG_FILE="/etc/systemd/network/10-$LAN_INTERFACE.link"
WAN_LINK_CONFIG_FILE="/etc/systemd/network/10-$WAN_INTERFACE.link"
LAN_ADDRESS="192.168.60.10/24"

sudo bash -c "cat > $LAN_LINK_CONFIG_FILE << EOF
[Match]
MACAddress=$LAN_MAC

[Link]
Name=$LAN_INTERFACE
EOF
"

sudo bash -c "cat > $WAN_LINK_CONFIG_FILE << EOF
[Match]
MACAddress=$WAN_MAC

[Link]
Name=$WAN_INTERFACE
EOF
"

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


