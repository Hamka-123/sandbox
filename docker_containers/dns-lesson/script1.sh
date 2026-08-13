#!/bin/bash

echo "Hello 1"
nslookup network_link

echo "Starting simple web server on port 8888..."

# Создаем простую страницу, которую увидим в браузере
echo "<h1>Hello from Docker!</h1><p>Container: $(hostname)</p>" > index.html

# Запускаем сервер:
# -p 8888 : слушаем порт 8888
# -f      : не уходим в фоновый режим (чтобы контейнер не закрылся)
# -h .    : отдаем файлы из текущей папки (наш index.html)
httpd -f -p 8888 -h .