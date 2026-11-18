#!/usr/bin/env bash
set -e

# Создаём и запускаем Jenkins
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -e JAVA_OPTS="-Xms256m -Xmx768m" \
  jenkins/jenkins:lts-jdk21

# Проверяем контейнер
docker ps
# Проверяем последние сообщения Jenkins
docker logs --tail 20 jenkins

# пароль генерится автоматически, смотрим его
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
# 710c095feebf4e5a81a6ab87bb827a9c

# в веб версии создаем админа с паролем и создаем токен
# апи токен 117d5ef0097e7a2356554667ebdde64971

# Сохраняем токен в переменную Bash
read -rsp "Вставь API-токен: " API_TOKEN
echo

# Делаем токен доступным другим командам
export API_TOKEN

# Проверяем авторизацию в Jenkins
curl -sS \
  -u "admin:$API_TOKEN" \
  http://localhost:8080/whoAmI/api/json
