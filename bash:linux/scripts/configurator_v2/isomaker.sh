sudo apt-get install -y genisoimage

# Создаем образ с поддержкой Linux-прав (-R)
genisoimage -o ~/octopus_net_v2.iso \
  -V "OCTOPUS_NET" \
  -R -J \
  ~/configurator_v2