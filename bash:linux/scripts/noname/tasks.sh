#Task
#Command
#Check if running
sudo systemctl status isc-dhcp-server
#Restart server
sudo systemctl restart isc-dhcp-server
#Test config syntax
sudo dhcpd -t -cf /etc/dhcp/dhcpd.conf
#Live log view
sudo tail -f /var/log/syslog | grep dhcpd
#Show all active IPs
dhcp-lease-list