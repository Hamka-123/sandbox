function Get-WSLSystemStatus {
    param ([string]$Distro = "Ubuntu")

    # Получаем память: выбираем строку Mem, делим по пробелам и убираем пустые элементы
    $memRaw = (wsl -d $Distro free -h | Select-String "Mem") -split '\s+' | Where-Object { $_ }
    
    # Получаем диск: берем последнюю строку вывода df
    $diskRaw = (wsl -d $Distro df -h / | Select-Object -Last 1) -split '\s+' | Where-Object { $_ }
    
    # Uptime в коротком формате
    $upRaw = (wsl -d $Distro uptime -p).Replace("up ", "").Trim()
    
    # Топ процесс: берем имя и %CPU, чистим от лишних пробелов
    $topProcRaw = (wsl -d $Distro bash -c "ps -eo comm,pcpu --sort=-pcpu | head -n 2 | tail -1").Trim()
    
    [PSCustomObject]@{
        Uptime     = $upRaw
        MemoryUsed = $memRaw[2]
        MemoryTotal= $memRaw[1]
        DiskUsed   = $diskRaw[2]
        DiskUsageP = $diskRaw[4] # Процент (например, 1%)
        TopProcess = $topProcRaw
    }
}