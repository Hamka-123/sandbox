#!/usr/bin/env bash
set -e

# Запускаем Jenkins без мастера настройки
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -e JAVA_OPTS="-Djenkins.install.runSetupWizard=false -Xms256m -Xmx768m" \
  jenkins/jenkins:lts-jdk21


# Проверяем, работает ли контейнер
docker ps
# Смотрим последние 20 строк логов Jenkins
docker logs --tail 20 jenkins
# Проверяем доступность Jenkins через HTTP
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  http://localhost:8080/login

# Останавливаем контейнер для безопасной настройки
docker stop jenkins

# Создаём скрипт настройки администратора
cat << 'EOF' > create-admin.groovy
import jenkins.model.*
import hudson.security.*
import jenkins.security.ApiTokenProperty
import java.security.SecureRandom
import java.util.Base64
import java.nio.file.Files
import java.nio.file.attribute.PosixFilePermissions

// Получаем Jenkins
def jenkins = Jenkins.get()

// Файл для сохранения пароля и токена
def credentials = new File(jenkins.rootDir, 'secrets/cli-admin.env')

// Создаём аккаунт только при первой настройке
if (!credentials.exists()) {

    // Генерируем случайный пароль
    byte[] randomBytes = new byte[24]
    new SecureRandom().nextBytes(randomBytes)
    def password = Base64.getUrlEncoder().withoutPadding().encodeToString(randomBytes)

    // Создаём администратора
    def realm = new HudsonPrivateSecurityRealm(false)
    def admin = realm.createAccount('admin', password)
    jenkins.setSecurityRealm(realm)

    // Запрещаем анонимный доступ
    def security = new FullControlOnceLoggedInAuthorizationStrategy()
    security.setAllowAnonymousRead(false)
    jenkins.setAuthorizationStrategy(security)

    // Получаем настройки API-токенов
    def property = admin.getProperty(ApiTokenProperty.class)
    if (property == null) {
        admin.addProperty(new ApiTokenProperty())
        property = admin.getProperty(ApiTokenProperty.class)
    }

    // Генерируем API-токен
    def token = property.tokenStore.generateNewToken('killercoda-cli').plainValue

    // Сохраняем настройки Jenkins
    admin.save()
    jenkins.save()

    // Создаём защищённый файл
    credentials.parentFile.mkdirs()
    Files.createFile(
        credentials.toPath(),
        PosixFilePermissions.asFileAttribute(
            PosixFilePermissions.fromString('rw-------')
        )
    )

    // Сохраняем пароль и токен
    credentials.text = "export JENKINS_ADMIN_PASSWORD='${password}'\nexport API_TOKEN='${token}'\n"

    println '[SUCCESS] Администратор и API-токен созданы.'
}
EOF

# Копируем скрипт в Jenkins
docker cp create-admin.groovy jenkins:/var/jenkins_home/init.groovy
# Запускаем Jenkins заново
docker start jenkins
# Проверяем журнал запуска
docker logs --tail 30 jenkins

# Загружаем пароль и токен из Jenkins
source <(docker exec -u 0 jenkins cat /var/jenkins_home/secrets/cli-admin.env)

# Проверяем, что токен загружен
test -n "${API_TOKEN:-}" && echo "API_TOKEN загружен"

# Проверяем авторизацию через Jenkins API
curl -sS -o /dev/null -w "HTTP %{http_code}\n" \
  -u "admin:$API_TOKEN" \
  http://localhost:8080/api/json

# Проверяем выполнение Groovy через CLI
# Отправляем Groovy-команду в Jenkins
curl -fsS -X POST \
  -u "admin:$API_TOKEN" \
  --data-urlencode "script=println 'JENKINS_CLI_READY'" \
  http://localhost:8080/scriptText
