$scriptPath = "$PSScriptRoot\scheduled-wsl-monitor.ps1"
$taskName = "WSLMonitoringLab"

# 1. Удаляем задачу, если она уже существует (чтобы избежать ошибок при повторном запуске скрипта)
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Предыдущая задача удалена." -ForegroundColor Yellow
}

# 2. Определяем действие
$action = New-ScheduledTaskAction -Execute "pwsh.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`""

# 3. Определяем триггер (старт через 1 минуту, повтор каждые 5 минут)
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 5)

# 4. Регистрация задачи
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -RunLevel Highest
Write-Host "Задача '$taskName' успешно зарегистрирована." -ForegroundColor Green

# 5. Принудительный запуск для мгновенной проверки
Start-ScheduledTask -TaskName $taskName
Write-Host "Выполняется тестовый запуск задачи... подождите 5 секунд." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# 6. Финальная проверка статуса
$taskInfo = Get-ScheduledTask -TaskName $taskName | Get-ScheduledTaskInfo
$taskInfo | Select-Object TaskName, LastRunTime, LastTaskResult, NextRunTime

if ($taskInfo.LastTaskResult -eq 0) {
    Write-Host "Тест пройден успешно! (Код 0)" -ForegroundColor Green
} else {
    Write-Host "Задача запущена, текущий код: $($taskInfo.LastTaskResult). Проверьте лог через минуту." -ForegroundColor Gray
}

# разово запустить задачу 
# Start-ScheduledTask -TaskName "WSLMonitoringLab"

# Посмотреть статус задачи 
# Get-ScheduledTask -TaskName "WSLMonitoringLab" | Get-ScheduledTaskInfo

# удалить задачу
# Unregister-ScheduledTask -TaskName "WSLMonitoringLab" -Confirm:$false