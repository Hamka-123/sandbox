#  sudo apt install isc-dhcp-server

To default config file insert include command:
include "/etc/dhcp/net192.168.60.conf"

subnet 192.168.60.0 netmask 255.255.255.0 {
  	range 192.168.60.1 192.168.60.254
  	option routers 192.168.60.10;
	option domain-name "net60.local";
	option domain-name-servers 192.168.60.10 1.1.1.1;


}
