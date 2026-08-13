#  nftables settings
NFT_FILE="/etc/nftables.conf"
# settings text:

# STEP 1: enable forwarding
# Substitute /etc/sysctl.conf/  line: #net.ipv4.ip_forward=1 to net.ipv4.ip_forward=1

# Check before changing:
sysctl net.ipv4.ip_forward
# Change
sudo sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf
# persist (apply)
sudo sysctl -p
# Check after changing
echo "New forwarding settings: $(sysctl net.ipv4.ip_forward)"

# STEP 2: set nftales tables:
sudo tee "$NFT_FILE" > /dev/null <<REM
#!/usr/sbin/nft -f

flush ruleset

# FILTER TABLE
table inet filter {

    chain input {
        type filter hook input priority 0;
        policy drop;
        iif lo accept
        ct state established,related accept
    }

    chain forward {
        type filter hook forward priority 0;
        policy drop;

        # LAN → WAN
        iif LAN oif WAN accept

        # WAN → LAN (return)
        iif WAN oif LAN ct state established,related accept
    }

    chain output {
        type filter hook output priority 0;
        policy accept
    }
}

# NAT TABLE
table ip nat {

    chain postrouting {
        type nat hook postrouting priority 100;
        oif WAN masquerade
    }
}

REM



# STEP:   reload , restart service
sudo systemctl enable nftables
sudo systemctl restart nftables

echo "nftables config written and applied."
