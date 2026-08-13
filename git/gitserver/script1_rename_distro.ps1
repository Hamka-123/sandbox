# --------------------------------------------
# Rename-WSL.ps1
# --------------------------------------------
<#
Permanently changes the Linux hostname
Updates /etc/hosts
Optionally changes the Windows-visible WSL distro name
PowerShell + Bash  Script

How to use
Example 1 - only change the Linux hostname:
.\script1_rename_distro.ps1 -DistroName "GitDeveloper1" -NewHostname "GitDeveloper1"
.\script1_rename_distro.ps1 -DistroName "GitServer" -NewHostname "GitServer"

Example 2 - change the Linux hostname and the Windows-visible distro name:
.\script1_rename_distro.ps1 -DistroName "Ubuntu1" -NewHostname "git_server" -NewDistroName "GitServer"
.\script1_rename_distro.ps1 -DistroName "Ubuntu4" -NewHostname "git_Developer1" -NewDistroName "GitDeveloper1"

Verification:
WSL Reset:
wsl --shutdown

wsl -d GitServer -- hostname

wsl --list --verbose
#>

param (
    [Parameter(Mandatory=$true)]
    [string]$DistroName,        # Windows-visible WSL distro name
    [Parameter(Mandatory=$true)]
    [string]$NewHostname,       # New Linux hostname
    [string]$NewDistroName      # Optional: new Windows-visible distro name
)

# Step 1: Run Bash inside WSL to change hostname permanently
wsl -d $DistroName -- bash -c "
echo '$NewHostname' | sudo tee /etc/hostname > /dev/null
sudo sed -i 's/127\.0\.1\.1.*/127.0.1.1   $NewHostname/' /etc/hosts
sudo hostnamectl set-hostname $NewHostname
"

Write-Host "[+] Linux hostname inside $DistroName changed to $NewHostname"

# Step 2: Optional - rename WSL distro in Windows
if ($NewDistroName) {
    $TempExport = "$env:TEMP\$DistroName.tar"
    
    Write-Host "[*] Exporting $DistroName to temporary file..."
    wsl --export $DistroName $TempExport

    Write-Host "[*] Unregistering old distro..."
    wsl --unregister $DistroName

    Write-Host "[*] Importing as $NewDistroName..."
    $InstallFolder = "$env:LOCALAPPDATA\WSL\$NewDistroName"
    New-Item -ItemType Directory -Force -Path $InstallFolder | Out-Null
    wsl --import $NewDistroName $InstallFolder $TempExport

    Remove-Item $TempExport
    Write-Host "[+] Windows-visible distro name changed to $NewDistroName"
}

Write-Host "[+] Done! Restart WSL to see changes."
