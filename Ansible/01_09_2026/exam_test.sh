#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

check_pass() {
    echo -e "[ ${GREEN}PASS${NC} ] $1"
    ((PASSED++))
}

check_fail() {
    echo -e "[ ${RED}FAIL${NC} ] $1"
    ((FAILED++))
}

echo "===================================================="
echo "    Ansible Exam Lab - Automated Verification Tool   "
echo "===================================================="

# Проверка рабочей директории / перехода в нее
if [ -d "ansible-exam-lab" ]; then
    cd ansible-exam-lab
    check_pass "Рабочая директория ansible-exam-lab найдена, переходим в нее."
elif [ -f "inventory.ini" ] || [ -d "roles" ]; then
    check_pass "Скрипт запущен изнутри папки ansible-exam-lab."
else
    check_fail "Папка ansible-exam-lab не найдена. Убедитесь, что запускаете из правильного места."
    exit 1
fi

echo ""
echo "--- Phase 1: Environment & Inventory Setup ---"

# 1. inventory.ini
if [ -f "inventory.ini" ]; then
    if grep -q "\[webservers\]" inventory.ini && grep -q "\[database\]" inventory.ini && grep -q "\[production:children\]" inventory.ini; then
        check_pass "inventory.ini содержит группы [webservers], [database] и [production:children]."
    else
        check_fail "inventory.ini существует, но в нем отсутствуют обязательные группы."
    fi
else
    check_fail "Файл inventory.ini отсутствует."
fi

# 2. .vault_pass и права 600
if [ -f ".vault_pass" ]; then
    PERMS=$(stat -c "%a" .vault_pass 2>/dev/null || stat -f "%A" .vault_pass 2>/dev/null)
    if [ "$PERMS" = "600" ]; then
        check_pass "Файл .vault_pass существует и имеет права 600."
    else
        check_fail "Файл .vault_pass имеет права $PERMS (требуется 600)."
    fi
    
    # Проверка на отсутствие перевода строки
    if [ -n "$(tail -c 1 .vault_pass)" ]; then
        check_pass "Файл .vault_pass не содержит завершающего символа новой строки (trailing newline)."
    else
        check_fail "Файл .vault_pass содержит перевод строки в конце."
    fi
else
    check_fail "Файл .vault_pass не найден."
fi

# 3. .gitignore
if [ -f ".gitignore" ] && grep -q "\.vault_pass" .gitignore; then
    check_pass ".gitignore содержит запись о скрытии .vault_pass."
else
    check_fail ".gitignore не найден или не содержит .vault_pass."
fi


echo ""
echo "--- Phase 2: Role Creation & Templating ---"

# 1. Структура роли webapp
if [ -d "roles/webapp" ] && [ -d "roles/webapp/defaults" ] && [ -d "roles/webapp/tasks" ] && [ -d "roles/webapp/handlers" ] && [ -d "roles/webapp/templates" ]; then
    check_pass "Структура роли webapp создана корректно."
else
    check_fail "Нарушена структура папок роли webapp."
fi

# 2. defaults/main.yml
if [ -f "roles/webapp/defaults/main.yml" ]; then
    if grep -q "app_port" roles/webapp/defaults/main.yml && grep -q "app_title" roles/webapp/defaults/main.yml; then
        check_pass "Переменные app_port и app_title определены в defaults/main.yml."
    else
        check_fail "В defaults/main.yml не хватает app_port или app_title."
    fi
else
    check_fail "Файл roles/webapp/defaults/main.yml отсутствует."
fi

# 3. Шаблон index.html.j2
if [ -f "roles/webapp/templates/index.html.j2" ]; then
    TPL="roles/webapp/templates/index.html.j2"
    if grep -q "app_title" "$TPL" && grep -q "ansible_hostname" "$TPL" && grep -q "ansible_default_ipv4" "$TPL" && grep -q "groups" "$TPL"; then
        check_pass "Шаблон index.html.j2 содержит все требуемые поля и цикл."
    else
        check_fail "В index.html.j2 отсутствуют некоторые обязательные параметры Jinja2."
    fi
else
    check_fail "Файл roles/webapp/templates/index.html.j2 отсутствует."
fi

# 4. tasks/main.yml роли
if [ -f "roles/webapp/tasks/main.yml" ]; then
    check_pass "Файл tasks/main.yml для роли webapp присутствует."
else
    check_fail "Файл roles/webapp/tasks/main.yml отсутствует."
fi


echo ""
echo "--- Phase 3: Resilient Logic & Error Handling ---"

if [ -f "maintenance_check.yml" ]; then
    if grep -q "loop" maintenance_check.yml && grep -q "block:" maintenance_check.yml && grep -q "rescue:" maintenance_check.yml && grep -q "always:" maintenance_check.yml; then
        check_pass "Playbook maintenance_check.yml содержит блок, rescue, always и loop."
    else
        check_fail "В maintenance_check.yml не найдена требуемая логика блоков обработки ошибок или циклов."
    fi
    
    # Проверка синтаксиса плейбука
    if ansible-playbook maintenance_check.yml --syntax-check &>/dev/null; then
        check_pass "Синтаксис maintenance_check.yml корректен (syntax-check пройден)."
    else
        check_fail "Ошибка синтаксиса в maintenance_check.yml."
    fi
else
    check_fail "Файл maintenance_check.yml отсутствует."
fi


echo ""
echo "--- Phase 4: Security & Vault Controls ---"

VAULT_FILE="group_vars/production/vault.yml"
if [ -f "$VAULT_FILE" ]; then
    # Проверка, зашифрован ли файл
    if head -n 1 "$VAULT_FILE" | grep -q "\$ANSIBLE_VAULT"; then
        check_pass "Файл group_vars/production/vault.yml успешно зашифрован Ansible Vault."
    else
        check_fail "Файл group_vars/production/vault.yml существует, но НЕ зашифрован."
    fi
else
    check_fail "Файл group_vars/production/vault.yml не найден."
fi

if [ -f "deploy_db_credentials.yml" ]; then
    if grep -q "no_log: true" deploy_db_credentials.yml || grep -q "no_log: True" deploy_db_credentials.yml; then
        check_pass "Директива no_log: true найдена в deploy_db_credentials.yml."
    else
        check_fail "В deploy_db_credentials.yml отсутствует no_log: true."
    fi
    
    if ansible-playbook deploy_db_credentials.yml --vault-password-file .vault_pass --syntax-check &>/dev/null; then
        check_pass "Синтаксис deploy_db_credentials.yml корректен."
    else
        check_fail "Ошибка синтаксиса в deploy_db_credentials.yml (проверьте пароль Vault)."
    fi
else
    check_fail "Файл deploy_db_credentials.yml отсутствует."
fi


echo ""
echo "--- Phase 5: Zero-Downtime Rolling Deployment ---"

if [ -f "site_deploy.yml" ]; then
    if grep -q "serial: 1" site_deploy.yml && grep -q "pre_tasks" site_deploy.yml && grep -q "post_tasks" site_deploy.yml && grep -q "webapp" site_deploy.yml; then
        check_pass "site_deploy.yml содержит serial: 1, pre_tasks, post_tasks и роль webapp."
    else
        check_fail "В site_deploy.yml не хватает конфигурации rolling update (serial/pre/post_tasks)."
    fi

    if ansible-playbook site_deploy.yml --vault-password-file .vault_pass --syntax-check &>/dev/null; then
        check_pass "Главный плейбук site_deploy.yml прошел проверку синтаксиса."
    else
        check_fail "Ошибка синтаксиса в site_deploy.yml."
    fi
else
    check_fail "Файл site_deploy.yml отсутствует."
fi

echo ""
echo "===================================================="
echo -5 "Итоговый отчет проверки:"
echo -e "Пройдено тестов: ${GREEN}$PASSED${NC}"
echo -e "Провалено тестов: ${RED}$FAILED${NC}"
echo "===================================================="

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}Поздравляем! Все критерии задания выполнены идеально!${NC}"
    exit 0
else
    echo -e "${YELLOW}Есть замечания. Исправьте ошибки, указанные выше.${NC}"
    exit 1
fi