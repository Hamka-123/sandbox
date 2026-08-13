🚀 Полный цикл: От локальной разработки до Production сервера
Шаг 1: Локальная разработка (Mac)
Создай проект: Создай папку и файлы server.py, index.html, папку js/ с файлом script.js.

Код сервера: Используй порт 9999 (чтобы избежать конфликтов в macOS).

Проверь локально: Запусти python3 server.py и открой http://localhost:9999.

Шаг 2: Перенос кода на сервер (2 варианта)
Вариант А: Через Git (Рекомендуемый)
На Маке:

Bash

git add .
git commit -m "Deploy: setup web server"
git push origin main
На Linux:

Bash

cd ~
git clone <url_репозитория>
cd <название_папки>
Вариант Б: Через SSH/SCP (Вручную)
Отправь папку с Мака прямо на сервер:

Bash

scp -r ./PythonWebProject hamka@IP_СЕРВЕРА:/home/hamka/
Шаг 3: Настройка системы (Linux)
1. Открой порт в Firewall (nftables)
Отредактируй /etc/nftables.conf, добавь tcp dport 9999 accept в цепочку input и примени:

Bash

sudo nft -f /etc/nftables.conf
2. Создай системную службу (Systemd)
Создай файл: sudo nano /etc/systemd/system/my_web_server.service

Вставь этот текст:

Ini, TOML

[Unit]
Description=Python Web Server
After=network.target

[Service]
User=hamka
WorkingDirectory=/home/hamka/PythonWebProject
ExecStart=/usr/bin/python3 /home/hamka/PythonWebProject/server.py
Restart=always

[Install]
WantedBy=multi-user.target
Шаг 4: Запуск и Проверка
Активируй службу:

Bash

sudo systemctl daemon-reload
sudo systemctl enable my_web_server
sudo systemctl start my_web_server
Проверь статус:

Bash

sudo systemctl status my_web_server
Проверь доступ извне: В браузере на Маке: http://IP_СЕРВЕРА:9999



1. Просто остановить (до следующей перезагрузки)
Эта команда мгновенно выключает сервер, но если ты перезагрузишь сам Linux-сервер, сервис запустится снова автоматически.

Bash

sudo systemctl stop my_web_server
2. Остановить и отключить автозапуск
Если ты хочешь полностью выключить сервис, чтобы он больше не запускался сам при старте системы:

Bash

sudo systemctl stop my_web_server    # Остановить сейчас
sudo systemctl disable my_web_server # Убрать из автозагрузки
3. Перезапустить (если изменила код)
Если ты обновила код через git pull и хочешь, чтобы изменения вступили в силу:

Bash

sudo systemctl restart my_web_server
4. Проверить состояние
Чтобы убедиться, что сервис действительно остановился (статус должен быть inactive (dead)):

Bash

sudo systemctl status my_web_server