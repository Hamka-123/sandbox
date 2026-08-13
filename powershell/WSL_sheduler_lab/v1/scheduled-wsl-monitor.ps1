# # 1. Подключаем файл с функцией (должен лежать в той же папке)
# . "$PSScriptRoot\Get-WSLSystemStatus.ps1"

# # 2. Получаем данные через функцию
# $status = Get-WSLSystemStatus -Distro "Ubuntu"

# # 3. Формируем текстовый блок для записи и записываем его в лог
# @"
# [$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")]
# Uptime:      $($status.Uptime)
# Memory:      $($status.Memory)
# Disk:        $($status.Disk)
# Top Process: $($status.TopProcess)
# ------------------------------------------------------------
# "@ | Out-File "$PSScriptRoot\scheduled-wsl-monitor.log" -Append -Encoding utf8

. "$PSScriptRoot\Get-WSLSystemStatus.ps1"
$status = Get-WSLSystemStatus -Distro "Ubuntu"

# Используем выравнивание через пробелы для красоты
@"
============================================================
TIMESTAMP:   $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
------------------------------------------------------------
UPTIME:      $($status.Uptime)
MEMORY:      $($status.Memory)
DISK:        $($status.Disk)
TOP PROCESS: $($status.TopProcess)
============================================================
"@ | Out-File "$PSScriptRoot\scheduled-wsl-monitor.log" -Append -Encoding utf8