#!/bin/bash

# --- БЛОК УМНОЙ МИГРАЦИИ ---
FOLDER_NAME="octopus_config"
TARGET_DIR="/tmp/$FOLDER_NAME"

SCRIPT_PATH=$(realpath "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")

# Проверяем: если мы не в /tmp/octopus_config, значит пора переезжать
if [ "$SCRIPT_DIR" != "$TARGET_DIR" ]; then
    echo "--- Подготовка временной рабочей среды: $TARGET_DIR ---"
    
    # Создаем чистую папку
    rm -rf "$TARGET_DIR"
    mkdir -p "$TARGET_DIR"
    
    # Копируем всё содержимое (скрипты, папки, пакеты)
    cp -r "$SCRIPT_DIR"/* "$TARGET_DIR/"
    
    # Даем полные права, чтобы не было ошибок "Permission Denied"
    chmod -R 777 "$TARGET_DIR"
    
    echo "Перезапуск..."
    # Запускаем уже из /tmp
    cd "$TARGET_DIR" || exit
    exec sudo bash "$TARGET_DIR/autostart.sh" "$@"
    exit
fi

# Теперь мы официально работаем из /tmp/octopus_config
cd "$TARGET_DIR" || exit
# ---------------------------

# --- 3. ФУНКЦИЯ ЛОГОТИПА ---
show_logo() {
    clear
    local CYAN='\033[0;36m'
    local YELLOW='\033[1;33m'
    local NC='\033[0m'

    echo -e "${CYAN}"
    echo "                .---.          "
    echo "               /     \         "
    echo "              ( @   @ )        ---  LINUX NETWORK  ---"
    echo "               )  X  (         ---   CONFIGURATOR  ---"
    echo "             ./   -   \.       ---       v2.0      ---"
    echo "            /  \ / \ /  \      "
    echo "           / /  V   V  \ \     "
    echo "          ( (           ) )    Author: qababenko@gmail.com"
    echo "           \ \         / /     "
    echo "            \ \       / /      "
    echo "             \ \     / /       "
    echo -e "${NC}"
    echo -e "${YELLOW}      <<< OCTOPUS DEVOPS TOOL >>>${NC}\n"
}

# --- 4. ПОДГОТОВКА ИНТЕРФЕЙСА (WHIPTAIL) ---
if ! command -v whiptail &> /dev/null; then
    echo "Интерфейс whiptail не найден. Установка из локальных пакетов..."
    # Пытаемся установить пакеты из вложенной папки packages
    if ls ./packages/whiptail*.deb &>/dev/null; then
        sudo dpkg -i ./packages/libnewt*.deb ./packages/whiptail*.deb > /dev/null 2>&1
    fi
    
    if command -v whiptail &> /dev/null; then
        echo "Интерфейс успешно подготовлен."
    else
        echo "Предупреждение: whiptail не установлен. Интерфейс может не отображаться."
    fi
fi

# --- 5. НАСТРОЙКА ОКРУЖЕНИЯ ---
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Отчет кладем в корень папки пользователя для удобства
export REPORT_PATH="$REAL_HOME/machine_report.txt"
export CONF_FILE="/tmp/server.conf"

rm -f "$CONF_FILE" "$REPORT_PATH"

# --- 6. ПОДКЛЮЧЕНИЕ БИБЛИОТЕК ---
for lib in lib_install.sh lib_init.sh lib_apply.sh lib_report.sh; do
    if [ -f "./$lib" ]; then
        source "./$lib"
    else
        echo -e "${RED}Ошибка: Библиотека $lib не найдена в $(pwd)!${NC}"
        exit 1
    fi
done

# --- 7. ОСНОВНОЙ ЦИКЛ РАБОТЫ ---
show_logo
echo -e "${GREEN}=== Запуск автоматической конфигурации ===${NC}"

# Шаг 1: Опрос пользователя
choose_role
generate_config

# Шаг 2: Установка пакетов (оффлайн)
install_offline_packages "$ROLE"

# Шаг 3: Применение сетевых настроек
apply_settings

# Шаг 4: Формирование отчета
generate_final_report

# Финальный штрих: права на отчет
chown "$REAL_USER:$REAL_USER" "$REPORT_PATH" 2>/dev/null

echo -e "\n${GREEN}=== Конфигурация завершена! ===${NC}"
echo -e "Отчет сохранен в: ${CYAN}$REPORT_PATH${NC}"