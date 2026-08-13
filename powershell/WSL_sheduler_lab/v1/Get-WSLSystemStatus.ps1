# function Get-WSLSystemStatus {
#     param (
#         [string]$Distro = "Ubuntu"
#     )

#     # Формируем объект с данными
#     [PSCustomObject]@{
#         Time       = Get-Date -Format "HH:mm:ss"
#         Distro     = $Distro
#         Uptime     = (wsl -d $Distro uptime).Trim()
#         Memory     = (wsl -d $Distro free -h).Trim()
#         Disk       = (wsl -d $Distro df -h /).Trim()
#         TopProcess = (wsl -d $Distro bash -c "ps -eo pid,comm,%cpu --sort=-%cpu | head -n 3").Trim()
#     }
# }
function Get-WSLSystemStatus {
    param ([string]$Distro = "Ubuntu")

    # 1. Получаем память и убираем пустые элементы
    $memRaw = (wsl -d $Distro free -h | Select-String "Mem") -split '\s+' | Where-Object { $_ }
    # Теперь: [0]=Mem:, [1]=Total, [2]=Used, [3]=Free...

    # 2. Получаем диск и убираем пустые элементы
    $diskRaw = (wsl -d $Distro df -h / | select -Last 1) -split '\s+' | Where-Object { $_ }
    # Теперь: [0]=Filesystem, [1]=Size, [2]=Used, [3]=Avail, [4]=Use%

    # 3. Чистим Uptime и Процесс
    $upRaw = (wsl -d $Distro uptime -p).Replace("up ", "").Trim()
    $topProcRaw = (wsl -d $Distro bash -c "ps -eo comm,pcpu --sort=-pcpu | head -n 2 | tail -1").Trim()

    [PSCustomObject]@{
        Uptime     = $upRaw
        Memory     = "Used: $($memRaw[2]) / Total: $($memRaw[1]) (Free: $($memRaw[3]))"
        Disk       = "Used: $($diskRaw[2]) ($($diskRaw[4])) | Avail: $($diskRaw[3])"
        TopProcess = $topProcRaw
    }
}
# для запуска, в PS консоли: 
# . .\Get-WSLSystemStatus.ps1
# Get-WSLSystemStatus