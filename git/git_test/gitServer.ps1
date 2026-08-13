# --- Config ---
$Distro = "Ubuntu"
$DistroName = "GitServer2"
$HostName = $DistroName
$SSHPort = "2222"
$User = "hamka"
$GitRepoName = "project.git"
$gitUser = "git"
$gitPass = "1234"

# 1. Установка дистрибутива
Write-Host "1. Установка $Distro под именем $DistroName " -ForegroundColor Cyan
wsl --install $Distro --name $DistroName
wsl --terminate $DistroName

# 2. Настройка wsl.conf (Hostname)
Write-Host "2. Настройка wsl.conf..." -ForegroundColor Cyan
$WslConf = @"
[network]
hostname=$HostName
generateHosts=true
"@
$WslConf = $WslConf.Replace("`r`n", "`n")
wsl -d $DistroName -u root -e sh -c "printf '$WslConf' > /etc/wsl.conf"

# 3. Установка и настройка SSH
Write-Host "3. Установка и настройка SSH на порт $SSHPort..." -ForegroundColor Cyan
$SSHSetup = @"
apt update && apt install -y openssh-server
sed -i 's/^#\?Port .*/Port $SSHPort/' /etc/ssh/sshd_config
sed -i 's/^#\?ListenAddress .*/ListenAddress 0.0.0.0/' /etc/ssh/sshd_config
sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config

mkdir -p /etc/systemd/system/ssh.socket.d
printf "[Socket]\nListenStream=\nListenStream=$SSHPort\n" > /etc/systemd/system/ssh.socket.d/override.conf

systemctl daemon-reload
systemctl enable --now ssh.socket
service ssh restart
"@
$SSHSetup = $SSHSetup.Replace("`r`n", "`n")
wsl -d $DistroName -u root -e sh -c $SSHSetup

# 4. Установка Git
Write-Host "4. Установка Git..." -ForegroundColor Cyan
$GitSetup = "apt update && apt install -y git"
wsl -d $DistroName -u root -e sh -c $GitSetup

# 5. Создание пользователя git с паролем
Write-Host "5. Создание пользователя '$gitUser' с паролем..." -ForegroundColor Cyan

$UserScript = @"
# Создаем юзера без лишних вопросов
if ! id "$gitUser" >/dev/null 2>&1; then
    adduser --gecos "" --disabled-password $gitUser
fi

# Устанавливаем пароль (замени '1234' на свой)
echo "git:$gitPass" | chpasswd

mkdir -p /srv/$gitUser
chown -R git:git /srv/$gitUser
sudo -u git git init --bare /srv/$gitUser/$GitRepoName
"@

$UserScript = $UserScript.Replace("`r`n", "`n")
wsl -d $DistroName -u root -e bash -c $UserScript
wsl --terminate $DistroName

Write-Host "`n[ФИНАЛ] Проект $GitRepoName готов к работе!" -ForegroundColor Green
Write-Host "Сервер доступен по SSH на порту $SSHPort" -ForegroundColor Cyan