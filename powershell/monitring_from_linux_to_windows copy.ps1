$DISTRO = "Ubuntu"
$path = "/home/$(wsl -d $distro whoami)/load-tests"
$CPU_logfile = "$path/top-CPU-log.log"
$MEM_logfile = "$path/top-MEM-log.log"

function Run-Wsl {
    param([string]$cmd)
    wsl -d $DISTRO bash -c $cmd
}

function Get-Top-Process {
    param ([string]$Type, [int]$Count)
    $sortFlag = if ($Type -eq "CPU") { "%CPU" } else { "%MEM" }
    $color = if ($Type -eq "CPU") { "Yellow" } else { "Cyan" }
    $currentLog = if ($Type -eq "CPU") { $CPU_logfile } else { $MEM_logfile }
    
    $title = "`nTop $Count processes by $Type (Logged at $(Get-Date))"
    Write-Host $title -ForegroundColor $color
    
    $startLine = 8
    $endLine = $startLine + ($Count - 1)
    
    # Записываем в лог
    $linuxCmd = "{ echo '$title'; top -b -n 1 -o $sortFlag | sed -n '${startLine},${endLine}p'; } >> $currentLog"
    Run-Wsl $linuxCmd

    # Вывод в консоль
    Run-Wsl "top -b -n 1 -o $sortFlag | sed -n '7,${endLine}p'"
}

function Show-PowerShell-Stats {
    param ([string]$LogFile)
    wsl -d $DISTRO test -f $LogFile
    if ($LASTEXITCODE -ne 0) { return }

    Write-Host "`n--- Final Statistics for $LogFile ---" -ForegroundColor Green
    $content = wsl -d $DISTRO cat $LogFile
    $stats = $content | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("Top") -and -not $line.StartsWith("PID")) {
            $parts = $line -split '\s+'
            $processName = $parts[-1].Trim()
            if ($processName) { $processName }
        }
    } | Group-Object | Select-Object @{Name="Process"; Expression={$_.Name}}, @{Name="Hits"; Expression={$_.Count}} | Sort-Object Hits -Descending
    $stats | Format-Table -AutoSize
}

# --- Исполнение (Новый метод: PowerShell Background Jobs) ---
Write-Host "--- Starting Smart Monitoring & Stress Test ---" -ForegroundColor Blue
Run-Wsl "mkdir -p $path"
Run-Wsl "rm -f $CPU_logfile $MEM_logfile"

# 1. Запускаем нагрузку как ФОНОВУЮ ЗАДАЧУ POWERSHELL
Write-Host "[!] Launching CPU & MEM load in separate job..." -ForegroundColor Red
$job = Start-Job -ScriptBlock {
    param($d)
    # Эта задача будет держать WSL занятым
    # Запускаем CPU нагрузку и ОДНОВРЕМЕННО тяжелую запись на диск (dd)
    # Используем путь /tmp, чтобы точно хватило прав
    # !!! dd генерирует в основном нагрузку на CPU а не MEM (для MEM лучше использовать утилиту stress)
    wsl -d $d bash -c "yes > /dev/null & dd if=/dev/zero of=/tmp/heavy_test bs=1M count=5000"
} -ArgumentList $DISTRO

# Даем секунду "прогреться"
Start-Sleep -Seconds 2

# 2. Делаем замеры (теперь yes точно будет в списке!)
Write-Host "[!] Collecting data..." -ForegroundColor Magenta
for ($i=1; $i -le 3; $i++) {
    Write-Host "`n--- Snapshot #$i ---" -ForegroundColor Gray
    Get-Top-Process -Type "CPU" -Count 5
    Get-Top-Process -Type "MEM" -Count 5
    Start-Sleep -Seconds 2
}

# 3. Убиваем задачу и чистим Linux
Write-Host "`n[!] Cleaning up..." -ForegroundColor Green
Stop-Job $job
Remove-Job $job
Run-Wsl "killall -q yes"
Run-Wsl "rm -f /tmp/heavy_test"

# 4. Итог
Show-PowerShell-Stats -LogFile $CPU_logfile
Show-PowerShell-Stats -LogFile $MEM_logfile