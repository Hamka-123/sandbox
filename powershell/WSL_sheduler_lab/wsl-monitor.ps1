# 1. Собираем данные в машине по-умолчанию
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$uptime    = wsl uptime
$memory    = wsl free -h
$disk      = wsl df -h
# Топ 6 процессов по потреблению CPU
$processes = wsl bash -c "ps -eo pid,comm,pcpu,pmem --sort=-pcpu | head -n 6"

# 2. Формируем текстовый блок отчета
$output = @"
================= WSL MONITOR REPORT =================
Time: $timestamp

--- CPU Load & Uptime ---
$uptime

--- Memory Usage ---
$memory

--- Disk Usage ---
$disk

--- Top Processes (by CPU) ---
$processes
======================================================
"@

# 3. Вывод в консоль (чтобы видеть процесс) и запись в лог-файл
Write-Host $output
$output | Out-File "wsl-monitor.log" -Append -Encoding utf8