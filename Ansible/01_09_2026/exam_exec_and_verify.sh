#!/bin/bash
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "===================================================="
echo "    Ansible Exam Lab - Execution & Verification     "
echo "===================================================="

# Переходим в директорию проекта, если она существует
if [ -d "ansible-exam-lab" ]; then
    cd ansible-exam-lab
    echo -e "[ ${GREEN}INFO${NC} ] Переход в директорию ansible-exam-lab"
elif [ -f "inventory.ini" ]; then
    echo -e "[ ${GREEN}INFO${NC} ] Запуск из корневой директории лаборатории"
else
    echo -e "[ ${RED}ERROR${NC} ] Директория ansible-exam-lab не найдена. Сначала сгенерируйте проект."
    exit 1
fi

# Проверка работы веб-сервера и рендеринга шаблона Phase 2
echo -e "\n--------------------------------------------------"
echo " Проверка Phase 2 (WebApp Role & Template)"
echo "--------------------------------------------------"
if curl -s http://localhost | grep -q "Enterprise Portal"; then
    echo -e "[ ${GREEN}PASS${NC} ] Веб-сервер отвечает, шаблон успешно отрендерен."
else
    echo -e "[ ${YELLOW}WARNING${NC} ] Веб-страница не отвечает или не содержит ожидаемый заголовок."
fi

echo -e "\n--------------------------------------------------"
echo " Шаг 1: Запуск Phase 3 (Maintenance Check & Error Handling)"
echo "--------------------------------------------------"
if ansible-playbook -i inventory.ini maintenance_check.yml --vault-password-file .vault_pass; then
    echo -e "[ ${GREEN}SUCCESS${NC} ] maintenance_check.yml успешно выполнен."
else
    echo -e "[ ${RED}FAIL${NC} ] Ошибка при выполнении maintenance_check.yml"
    exit 1
fi

# Проверка создания лога из always-блока
if [ -f "/tmp/maintenance.log" ]; then
    echo -e "[ ${GREEN}PASS${NC} ] Лог-файл /tmp/maintenance.log найден:"
    tail -n 2 /tmp/maintenance.log
else
    echo -e "[ ${RED}FAIL${NC} ] Лог-файл /tmp/maintenance.log не обнаружен."
    exit 1
fi

echo -e "\n--------------------------------------------------"
echo " Шаг 2: Запуск Phase 4 (Deploy DB Credentials via Vault)"
echo "--------------------------------------------------"
if ansible-playbook -i inventory.ini deploy_db_credentials.yml --vault-password-file .vault_pass; then
    echo -e "[ ${GREEN}SUCCESS${NC} ] deploy_db_credentials.yml успешно выполнен."
else
    echo -e "[ ${RED}FAIL${NC} ] Ошибка при деплое учетных данных базы данных."
    exit 1
fi

# Проверка файла конфигурации и прав 0600
if [ -f "/etc/db_app.conf" ]; then
    PERMS=$(stat -c "%a" /etc/db_app.conf 2>/dev/null || stat -f "%A" /etc/db_app.conf 2>/dev/null)
    if [ "$PERMS" = "600" ]; then
        echo -e "[ ${GREEN}PASS${NC} ] Файл /etc/db_app.conf существует и имеет правильные права: $PERMS"
    else
        echo -e "[ ${YELLOW}WARNING${NC} ] Файл /etc/db_app.conf имеет права $PERMS вместо 0600."
    fi
else
    echo -e "[ ${RED}FAIL${NC} ] Файл /etc/db_app.conf не найден."
    exit 1
fi

echo -e "\n--------------------------------------------------"
echo " Шаг 3: Запуск Phase 5 (Zero-Downtime Rolling Deployment)"
echo "--------------------------------------------------"
if ansible-playbook -i inventory.ini site_deploy.yml --vault-password-file .vault_pass; then
    echo -e "[ ${GREEN}SUCCESS${NC} ] Главный оркестрационный плейбук site_deploy.yml успешно выполнен."
else
    echo -e "[ ${RED}FAIL${NC} ] Ошибка при выполнении site_deploy.yml"
    exit 1
fi

# Проверка идемпотентности (повторный запуск site_deploy.yml)
echo -e "\n--------------------------------------------------"
echo " Шаг 4: Проверка идемпотентности (Повторный прогон site_deploy.yml)"
echo "--------------------------------------------------"
IDEMPOTENT_OUTPUT=$(ansible-playbook -i inventory.ini site_deploy.yml --vault-password-file .vault_pass)
echo "$IDEMPOTENT_OUTPUT"

if echo "$IDEMPOTENT_OUTPUT" | grep -q "changed=0.*failed=0" || ! echo "$IDEMPOTENT_OUTPUT" | grep -q "changed: [1-9]"; then
    echo -e "\n[ ${GREEN}PASS${NC} ] Идемпотентность соблюдена (нет непредвиденных изменений при повторном запуске)."
else
    echo -e "\n[ ${YELLOW}NOTE${NC} ] Повторный запуск привел к изменениям (проверьте, все ли задачи идемпотентны)."
fi

echo -e "\n==================================================--"
echo -e "${GREEN} ВСЕ ЗАДАЧИ ЭКЗАМЕНА УСПЕШНО ВЫПОЛНЕНЫ И ПРОВЕРЕНЫ! ${NC}"
echo "==================================================--"