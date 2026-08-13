# --- Config ---
$DistroName = "GitDev1"
$UserName = "Dev"     
$UserEmail = "dev@example.com"
$ServerIP = "172.22.59.224"    
$SSHPort = "2222"
$RepoPath = "/srv/git/project.git"

# 1. Установка Git
Write-Host "1. Установка Git на клиент..." -ForegroundColor Cyan
wsl -d $DistroName -- sudo apt update
wsl -d $DistroName -- sudo apt install -y git

# 2. Настройка личности (Identity)
Write-Host "2. Настройка Git Identity..." -ForegroundColor Cyan
wsl -d $DistroName -- bash -c "git config --global user.name '$UserName' && git config --global user.email '$UserEmail'"

# 3. Создание проекта и инициализация
Write-Host "3. Создание проекта и Git Init..." -ForegroundColor Cyan
wsl -d $DistroName -- bash -c "mkdir -p ~/project1 && cd ~/project1 && git init"

# 4. Создание файлов
Write-Host "4. Наполнение проекта файлами..." -ForegroundColor Cyan
wsl -d $DistroName -- bash -c "cd ~/project1 && echo '# project1' > README.md && echo 'Hello from GitDeveloper1' > app.txt"

# 5. Первый коммит
Write-Host "5. Фиксация изменений (Commit)..." -ForegroundColor Cyan
wsl -d $DistroName -- bash -c "cd ~/project1 && git add . && git commit -m 'Initial commit'"

# 6. Привязка к серверу
Write-Host "6. Привязка удаленного репозитория..." -ForegroundColor Cyan
# Используем формат ssh:// для указания порта
$RemoteUrl = "ssh://git@${ServerIP}:${SSHPort}${RepoPath}"
wsl -d $DistroName -- bash -c "cd ~/project1 && git remote add origin $RemoteUrl"

# 7. Пуш на сервер
Write-Host "7. Пуш в ветку master..." -ForegroundColor Cyan
Write-Host "ВНИМАНИЕ: Потребуется ввод пароля пользователя git!" -ForegroundColor Yellow
wsl -d $DistroName -- bash -c "cd ~/project1 && git push -u origin master"

Write-Host "`n[УСПЕХ] Проект создан и отправлен на сервер!" -ForegroundColor Green