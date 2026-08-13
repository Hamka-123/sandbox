#!/bin/bash

# =================================================================
# ШПАРГАЛКА ПО DOCKER: СЕТИ, ТОМА И УПРАВЛЕНИЕ ПРОЦЕССАМИ
# =================================================================

# 1. ПОДГОТОВКА ИНФРАСТРУКТУРЫ (Infrastructure Setup)
# -----------------------------------------------------------------
# Создаем изолированную сеть, чтобы контейнеры видели друг друга по именам
docker network create lab_net

# Создаем именованный том (Named Volume) для постоянного хранения данных
docker volume create mariadb_data


# 2. ЗАПУСК КОНТЕЙНЕРОВ (Deployment)
# -----------------------------------------------------------------
# Запуск БД: -d (фон), --v (том), -e (переменные окружения для пароля)
docker run -d \
  --name mariadb_server \
  --network lab_net \
  -v mariadb_data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  mariadb

# Запуск админки: пробрасываем порт 8080 хоста на 80 контейнера
docker run -d \
  --name phpmyadmin \
  --network lab_net \
  -p 8080:80 \
  -e PMA_HOST=mariadb_server \
  phpmyadmin


# 3. ИССЛЕДОВАНИЕ "ПОД КАПОТОМ" (Deep Dive / Debug)
# -----------------------------------------------------------------
# Посмотреть детали тома (узнать Mountpoint в виртуальной машине)
docker volume inspect vol_test_1

# Магический вход внутрь виртуальной машины Docker Desktop (через пространство имен PID 1)
# Мы обходим изоляцию, чтобы увидеть файлы тома напрямую в /var/lib/docker/volumes/
# 
# docker run -it --privileged --pid=host debian nsenter -t 1 -m -u -n -i sh


# 4. МОНИТОРИНГ И УПРАВЛЕНИЕ (Processes & Sockets)
# -----------------------------------------------------------------
# Посмотреть активные сетевые соединения (сокеты) процесса Zoom на Маке
# lsof -iUDP | grep zoom

# Найти PID (Process ID), который ядро ОС закрепило за контейнером
docker inspect --format '{{.State.Pid}}' writer

# Остановить конкретный контейнер (посылает сигнал SIGTERM процессу)
docker stop writer


# 5. ГИГИЕНА СИСТЕМЫ (Cleanup)
# -----------------------------------------------------------------
# Остановить ВЕЕ запущенные контейнеры разом (через список ID)
# docker stop $(docker ps -q)

# Удалить всё неиспользуемое: контейнеры, сети и неиспользуемые образы
docker system prune

# Глобальная зачистка: включая тома (--volumes) и вообще все образы (-a)
# docker system prune -a --volumes

# backup
docker run --rm -v vol_test_1:/source_data -v $(pwd):/backup alpine tar -czf /backup/my_backup.tar.gz -C /source_data .
#pg backup pg_dump
docker exec postgres_server pg_dump -U postgres lab_db > lab_db_backup.sql

#restore backup
docker run --rm -v vol_test_2:/data -v $(pwd):/backup alpine sh -c "cd /data && tar xzf /backup/my_backup.tar.gz"
#restore pg pg_dump
cat lab_db_backup.sql | docker exec -i postgres_server psql -U postgres -d lab_db

# enter to db
docker exec -it mariadb_server mariadb -u root -p labdb

# Поле,Значение,Примечание
# Host,localhost,Твой Мак.
# Port,3306,Стандартный порт для MySQL/MariaDB.
# Database,labdb,Имя базы из -e MYSQL_DATABASE.
# Username,root,Суперпользователь.
# Password,rootpass,Пароль из -e MYSQL_ROOT_PASSWORD.

# Поле,Значение,Почему так?
# Host,localhost,База «торчит» наружу через порт твоего Мака.
# Port,5432,Стандартный порт Postgres.
# Database,lab_db,"Имя базы, которое мы указали в -e POSTGRES_DB."
# Username,postgres,Пользователь по умолчанию.
# Password,pgpass,Пароль из -e POSTGRES_PASSWORD.