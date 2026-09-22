#!/usr/bin/env bash
set -e

echo "=== 1. Updating OS & Installing Docker on Host ==="
sudo apt-get update && sudo apt-get install -y curl git ca-certificates

if ! command -v docker &> /dev/null; then
    sudo curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm -f get-docker.sh
fi

echo "=== 2. Cleaning Up Existing Container ==="
docker rm -f jenkins 2>/dev/null || true

echo "=== 3. Launching Jenkins Container ==="
docker run -d \
  --name jenkins \
  --restart always \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e JAVA_OPTS="-Djenkins.install.runSetupWizard=false -Dhudson.security.csrf.GlobalCrumbIssuerConfiguration.DISABLE_CSRF_PROTECTION=true" \
  jenkins/jenkins:lts-jdk17

echo "Waiting for Jenkins to initialize..."
sleep 15

echo "=== 4. Installing Docker CLI & Fixing Socket Permissions inside Container ==="
# Install docker CLI binary inside the container
docker exec -u 0 jenkins apt-get update
docker exec -u 0 jenkins apt-get install -y docker.io
# Grant access to socket
docker exec -u 0 jenkins chmod 666 /var/run/docker.sock

echo "=== 5. Pre-installing Jenkins Plugins ==="
docker exec jenkins jenkins-plugin-cli --plugins workflow-aggregator git docker-workflow github
docker restart jenkins

echo "=== DONE! Jenkins is ready at http://$(curl -s ifconfig.me):8080 ==="



# Поддержка Docker-out-of-Docker (DooD): Пробрасывает docker.sock и устанавливает Docker CLI внутрь контейнера, позволяя Jenkins собирать другие Docker-образы в процессе работы.

# Сохранение данных: Использует стандартный том /var/jenkins_home, благодаря чему настройки, история сборок и плагины не удаляются при перезапуске скрипта (во втором скрипте том жестко удаляется).

# Автоматическая установка плагинов: Сразу «из коробки» доустанавливает критически важные плагины (git, workflow-aggregator, docker-workflow) через jenkins-plugin-cli.

# Автоустановка Docker на хост: Сам проверяет наличие Docker на компьютере/сервере и при необходимости устанавливает его с нуля.

# Корректные системные пути: Примонтирует рабочую директорию в официальный путь (/var/jenkins_home), избегая конфликтов и падений контейнера.