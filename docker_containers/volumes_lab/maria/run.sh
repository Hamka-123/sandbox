#!/bin/bash

docker run -d \
--name mariadb_server \
--network lab_net \
-e MYSQL_ROOT_PASSWORD=rootpass \
-e MYSQL_DATABASE=labdb \
-v mariadb_data:/var/lib/mysql \
mariadb

docker run -d \
--name phpmyadmin \
--network lab_net \
-e PMA_HOST=mariadb_server \
-p 8080:80 \
phpmyadmin


docker run -d \
--name postgres_server \
--network lab_net \
-e POSTGRES_PASSWORD=pgpass \
-e POSTGRES_DB=lab_db \
-v pg_data:/var/lib/postgresql \
postgres

docker run -d \
--name postgres_server \
--network lab_net \
-e POSTGRES_PASSWORD=pgpass \
-v pg_data:/var/lib/postgresql/data \
postgres:17