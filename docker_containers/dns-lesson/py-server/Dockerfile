FROM python:3.11-slim

WORKDIR /app

# Копируем наш питоновский скрипт
COPY server.py .

# Открываем порт
EXPOSE 8888

# Запускаем сервер
CMD ["python", "server.py"]