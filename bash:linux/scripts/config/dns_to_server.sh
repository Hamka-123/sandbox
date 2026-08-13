#!/bin/bash

# Цвета для вывода (если они не определены в главном скрипте)
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Динамически получаем IP-адрес интерфейса LAN
# Берем адрес только IPv4 и убираем маску (/24)
LAN_IP=$(ip -4 addr show LAN1 | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n 1)

if [[ -z "$LAN_IP" ]]; then
    echo -e "${RED}❌ Ошибка: Не удалось определить IP интерфейса LAN${NC}"
    exit 1
fi

echo "Определен LAN1 IP: $LAN_IP"

# 2. Добавляем LAN IP в список прослушиваемых адресов для DNS
# Проверяем, нет ли уже этой настройки именно с этим IP
if ! grep -q "DNSStubListenerExtra=$LAN_IP" /etc/systemd/resolved.conf; then
    echo "Настраиваю systemd-resolved на прослушивание $LAN_IP..."
    
    # Удаляем старые записи DNSStubListenerExtra, если они были, чтобы не плодить мусор
    sudo sed -i '/DNSStubListenerExtra=/d' /etc/systemd/resolved.conf
    
    # Добавляем актуальную запись под секцию [Resolve]
    sudo sed -i "/\[Resolve\]/a DNSStubListenerExtra=$LAN_IP" /etc/systemd/resolved.conf
    
    # 3. Перезапускаем сервис
    sudo systemctl restart systemd-resolved
else
    echo "DNS уже настроен на прослушивание $LAN_IP."
fi

# 4. Проверка
if sudo ss -tulpn | grep -q "$LAN_IP:53"; then
    echo -e "${GREEN}✅ DNS теперь слушает на $LAN_IP${NC}"
else
    echo -e "${RED}❌ Ошибка: DNS не поднялся на интерфейсе $LAN_IP${NC}"
    exit 1
fi