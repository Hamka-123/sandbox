$DISTRO = "Ubuntu"
$path = "/home/$(wsl -d $distro whoami)"
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
    
    # 1. Формируем заголовок для консоли Windows
    $title = "`nTop $Count processes by $Type (Logged at $(Get-Date))"
    Write-Host $title -ForegroundColor $color
    
    # 2. Формируем команду для Linux
    $startLine = 8
    $endLine = $startLine + ($Count - 1)
    
    # Команда запишет и заголовок, и данные в файл внутри WSL
    if ($Type -eq "CPU"){
        # Мы используем { ... } >> file, чтобы отправить весь вывод сразу в лог
        $linuxCmd = "{ echo '$title'; top -b -n 1 -o $sortFlag | sed -n '${startLine},${endLine}p'; } >> $CPU_logfile"
    }
    else{
        $linuxCmd = "{ echo '$title'; top -b -n 1 -o $sortFlag | sed -n '${startLine},${endLine}p'; } >> $MEM_logfile"
    }
    
    Run-Wsl $linuxCmd

    # 3. Выведем в консоль только результат (для красоты)
    Run-Wsl "top -b -n 1 -o $sortFlag | sed -n '7,${endLine}p'"
}
function Show-Statistics {
    param ([string]$LogFile)
    Write-Host "`n--- Frequency of processes in $LogFile ---" -ForegroundColor Green
    
    # Мы используем одинарные кавычки для всей команды, чтобы $NF дошел до Linux живым
    # команда передается криво!!!
    $awkCmd = 'awk ''/^Top/ {next} NF>0 {count[$NF]++} END {for (p in count) print count[p], p}'' ' + $LogFile + ' | sort -rn'
    Run-Wsl $awkCmd
}
function Show-PowerShell-Stats {
    # собираем отчет в виндовсе
    param ([string]$LogFile)
    
    # Проверяем существование файла простым способом
    wsl -d $DISTRO test -f $LogFile
    if ($LASTEXITCODE -ne 0) { 
        Write-Host "Файл $LogFile не найден." -ForegroundColor Red
        return 
    }

    Write-Host "`n--- Final Statistics for $LogFile ---" -ForegroundColor Green

    $content = wsl -d $DISTRO cat $LogFile
    $stats = $content | ForEach-Object {
        $line = $_.Trim()
        # Пропускаем заголовки и пустые строки
        if ($line -and -not $line.StartsWith("Top") -and -not $line.StartsWith("PID")) {
            $parts = $line -split '\s+'
            $processName = $parts[-1].Trim() # Чистим имя процесса
            if ($processName) { $processName }
        }
    } | Group-Object | Select-Object @{Name="Process"; Expression={$_.Name}}, @{Name="Hits"; Expression={$_.Count}} | Sort-Object Hits -Descending

    $stats | Format-Table -AutoSize
}

function Start-Test-CPU-Load {
    Run-Wsl "yes > /dev/null &" 
}
function Stop-Test-CPU-Load {
    Run-Wsl "killall yes"
}

function Test-MEM-Load {
    param ([string]$value)
    Run-Wsl "dd if=/dev/zero of=io_test_file bs=1M count=$value conv=fdatasync"
    Run-Wsl "rm -f io_test_file"

}

# --- Исполнение с тестом ---
Write-Host "Starting monitoring and stress test..." -ForegroundColor Blue

# 1. Запускаем нагрузку на CPU
Write-Host "Applying CPU load..." -ForegroundColor Red
Start-Test-CPU-Load # !!! фоновый процесс завершается вместе с сессией wsl, потому нагрузка прекращается к моменту замеров.
Test-MEM-Load -value 500

Write-Host "Starting monitoring..." -ForegroundColor Blue
Run-Wsl "mkdir -p $path"

Run-Wsl "rm -f $CPU_logfile" # Очищаем старый лог перед запуском
Run-Wsl "rm -f $MEM_logfile" # Очищаем старый лог перед запуском

Get-Top-Process -Type "CPU" -Count 5
Get-Top-Process -Type "MEM" -Count 5

Stop-Test-CPU-Load

# Write-Host "`nFinal Log file inside WSL:" -ForegroundColor Gray
# Run-Wsl "cat $CPU_logfile"
# Run-Wsl "cat $MEM_logfile"

Show-PowerShell-Stats -LogFile $CPU_logfile
Show-PowerShell-Stats -LogFile $MEM_logfile