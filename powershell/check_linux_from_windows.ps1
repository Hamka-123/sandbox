$distro = "Ubuntu"
$path = "/home/$(wsl -d $distro whoami)"
$file = "my_new_file.log"

# Функция для удобного запуска, чтобы не писать каждый раз wsl -d ...
function Run-Wsl {
    param([string]$cmd)
    wsl -d $distro bash -c $cmd
}

# 1. Создаем папку
Write-Host "`n--- Step 1: folder and file ---" -ForegroundColor Cyan
Run-Wsl "mkdir -p $path"

# 2. Записываем дату
$currentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Run-Wsl "echo '$currentDate' > $path/$file"
Write-Host "File created $path/$file" -ForegroundColor Green

# 3. Вывод содержимого
Write-Host "`n--File content:" -ForegroundColor Cyan
Run-Wsl "cat $path/$file"

# 4. Проверка ресурсов
Write-Host "`n--- Step 2: check resources ---" -ForegroundColor Cyan
#Проверка свободного места
Run-Wsl "df -h /"

# Список открытых портов
Write-Host "`n--Ports:" -ForegroundColor Cyan
Run-Wsl "ss -tuln"

# 5. проверка SSH
Write-Host "`n--- Step 3: check ssh ---" -ForegroundColor Cyan
# --- Проверка SSH КЛИЕНТА ---
$checkSshClient = Run-Wsl "command -v ssh"
if ([string]::IsNullOrEmpty($checkSshClient)) {
    Write-Host "SSH Client missing. Installing..." -ForegroundColor Yellow
    Run-Wsl "sudo apt update && sudo apt install openssh-client -y"
} else {
    $clientVersion = Run-Wsl "ssh -V 2>&1"
    # 2>&1 - Это важный технический момент: команда ssh -V почему-то выводит информацию о версии не в стандартный поток (stdout), 
    # а в поток ошибок (stderr). Если не добавить 2>&1, PowerShell может подумать, что команда вернула пустоту, 
    # хотя на самом деле версия есть.
    Write-Host "SSH Client is OK: $clientVersion" -ForegroundColor Gray
}

# --- Проверка SSH СЕРВЕРА ---
$checkSshServer = Run-Wsl "command -v sshd"
if ([string]::IsNullOrEmpty($checkSshServer)) {
    Write-Host "SSH Server missing. Installing..." -ForegroundColor Yellow
    Run-Wsl "sudo apt update && sudo apt install openssh-server -y"
} else {
    Write-Host "SSH Server is installed." -ForegroundColor Cyan
}
# 4. Статус и запуск
Write-Host "`n--- Step 4: ssh server service status ---" -ForegroundColor Cyan
# Пытаемся запустить на случай, если он просто был выключен
Run-Wsl "sudo service ssh start" 
# Показываем статус (только для ssh)
Run-Wsl "systemctl status ssh -l --no-pager"