# WSL specific !!!!!!!!!!!!
wsl -d GitServer -- sudo mkdir -p /run/sshd
wsl -d GitServer -- sudo chmod 0755 /run/sshd


wsl -d GitServer -- sudo bash -c "cat > /etc/ssh/sshd_config <<'EOF'
Port 2222
ListenAddress 0.0.0.0
Protocol 2

PermitRootLogin no
PasswordAuthentication yes
PubkeyAuthentication yes

UsePAM yes
Subsystem sftp /usr/lib/openssh/sftp-server
EOF"

wsl -d GitServer -- sudo /usr/sbin/sshd

# Check SSH listening ...
wsl -d GitServer -e sh -c "ss -tlnp | grep 2222"

# Enable SSH
wsl -d GitServer -- sudo systemctl enable ssh
wsl -d GitServer -- sudo systemctl start ssh

# Status:
wsl -d GitServer -- sudo systemctl status ssh
