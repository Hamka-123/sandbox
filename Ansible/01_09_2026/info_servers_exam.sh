#!/bin/bash
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Переход в рабочую директорию
if [ -d "ansible-exam-lab" ]; then
    cd ansible-exam-lab
elif [ -f "inventory.ini" ]; then
    true
else
    echo "Директория проекта не найдена."
    exit 1
fi

VAULT_PASS_ARG="--vault-password-file .vault_pass"

echo -e "${BLUE}=== 1. ПИНГ И ДОСТУПНОСТЬ ХОСТОВ ===${NC}"
ansible production -i inventory.ini -m ping $VAULT_PASS_ARG
echo ""

echo -e "${BLUE}=== 2. СИСТЕМНАЯ ИНФОРМАЦИЯ И АПТАЙМ ===${NC}"
ansible production -i inventory.ini -m command -a "uptime" $VAULT_PASS_ARG
echo ""

echo -e "${BLUE}=== 3. СОСТОЯНИЕ ДИСКОВОГО ПРОСТРАНСТВА ===${NC}"
ansible production -i inventory.ini -m shell -a "df -h /" $VAULT_PASS_ARG
echo ""

echo -e "${BLUE}=== 4. СТАТУС ВЕБ-СЕРВЕРОВ И СЛУЖБ ===${NC}"
ansible webservers -i inventory.ini -m shell -a "systemctl is-active apache2 || systemctl is-active httpd" $VAULT_PASS_ARG
echo ""

echo -e "${BLUE}=== 5. ПРОВЕРКА ПРАВ ФАЙЛА КОНФИГУРАЦИИ БД (/etc/db_app.conf) ===${NC}"
ansible database -i inventory.ini -m shell -a "ls -la /etc/db_app.conf" $VAULT_PASS_ARG
echo ""

echo -e "${BLUE}=== 6. ПОСЛЕДНИЕ ЗАПИСИ В ЛОГЕ ОБСЛУЖИВАНИЯ ===${NC}"
ansible production -i inventory.ini -m shell -a "tail -n 3 /tmp/maintenance.log 2>/dev/null || echo 'Лог пока отсутствует'" $VAULT_PASS_ARG
echo ""

echo -e "${BLUE}=== 7. ДОСТУПНОСТЬ ЛОКАЛЬНОГО HTTP-СЕРВЕРА ===${NC}"
ansible webservers -i inventory.ini -m shell -a "curl -sI http://localhost | head -n 5" $VAULT_PASS_ARG
echo ""

echo -e "${BLUE}=== 8. СОДЕРЖИМОЕ СГЕНЕРИРОВАННОЙ ВЕБ-СТРАНИЦЫ ===${NC}"
ansible webservers -i inventory.ini -m shell -a "curl -s http://localhost" $VAULT_PASS_ARG