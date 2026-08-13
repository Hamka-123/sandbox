#  nftables settings

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
: <<REM


REM



# STEP:   reload , restart service
