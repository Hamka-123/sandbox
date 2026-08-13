Restart-Service LxssManager
Pause
Restart-Service vmcompute -Force
Pause 'LxssManager restarted ...' 
Get-Service | Where-Object {
    $_.Name -in @("LxssManager", "vmcompute")
} | Restart-Service -Force
