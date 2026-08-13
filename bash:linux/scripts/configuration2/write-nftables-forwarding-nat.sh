#!/bin/bash
set -euo pipefail

NFT_FILE="/etc/nftables.conf"

# === Backup existing config ===
if [ -f "$NFT_FILE" ]; then
    sudo cp "$NFT_FILE" "$NFT_FILE.bak.$(date +%F_%H%M%S)"
    echo "Backup created: $NFT_FILE.bak.*"
fi

# === Write nftables config ===
sudo tee "$NFT_FILE" > /dev/null <<'EOF'
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
EOF

# === Enable & restart nftables ===
sudo systemctl enable nftables
sudo systemctl restart nftables

echo "✅ nftables config written and applied."
