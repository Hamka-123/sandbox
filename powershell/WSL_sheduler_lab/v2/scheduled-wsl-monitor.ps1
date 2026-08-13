# 1. Подключаем функцию
. "$PSScriptRoot\Get-WSLSystemStatus.ps1"

# 2. Получаем данные
$status = Get-WSLSystemStatus -Distro "Ubuntu"

# 3. Анализ CPU для алерта (извлекаем число из конца строки, например "ps 4.6")
$cpuValue = [float]($status.TopProcess -split '\s+')[-1]
$systemStatus = if ($cpuValue -gt 50.0) { "WARNING" } elseif ($cpuValue -gt 90.0) { "CRITICAL" } else { "OK" }

# 4. Формируем объект для экспорта
$logData = [PSCustomObject]@{
    Timestamp   = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Status      = $systemStatus
    CPU_Percent = $cpuValue
    Uptime      = $status.Uptime
    RAM_Used    = $status.MemoryUsed
    RAM_Total   = $status.MemoryTotal
    Disk_Usage  = $status.DiskUsageP
    Top_Process = $status.TopProcess
}

# 5. Путь к файлу с ротацией по дате
$currentDate = Get-Date -Format "yyyy-MM-dd"
$csvFileName = "$PSScriptRoot\wsl-monitor-$currentDate.csv"

# 6. Запись в CSV
$logData | Export-Csv -Path $csvFileName -Append -NoTypeInformation -Encoding utf8

# Если статус WARNING, можно подать звуковой сигнал (опционально)
if ($systemStatus -eq "WARNING") { [System.Console]::Beep(440, 500) }

# Удаление старых логов (старше 30 дней)
Get-ChildItem "$PSScriptRoot\wsl-monitor-*.csv" | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | Remove-Item

