param(
	$DownloadURL = "https://windows.metasploit.com/metasploitframework-latest.msi",
	$DownloadLocation = "$env:APPDATA/Metasploit",
	$InstallLocation = "C:\Tools",
	$LogLocation = "$DownloadLocation/install.log"
)

# Display a message at the beginning
Write-Host "This script will download and install Metasploit. Please do not close this window until the installation is complete."

# Function to run a command as administrator
function Run-As-Administrator {
	param(
		[string]$Command
	)

	# Create a new process to run the command as administrator
	Start-Process -FilePath PowerShell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command `"$Command`"" -Verb RunAs
}

# Check if the script is running as administrator
$IsAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

# If not running as administrator, relaunch the script with administrator privileges
if (-not $IsAdmin) {
	$ScriptPath = $MyInvocation.MyCommand.Path
	Start-Process powershell.exe -ArgumentList "-ExecutionPolicy Bypass -File $ScriptPath" -Verb RunAs -Wait
	exit
}

# Check and create directories if they don't exist
if (-not (Test-Path $DownloadLocation)) {
	New-Item -Path $DownloadLocation -ItemType Directory
}

if (-not (Test-Path $InstallLocation)) {
	New-Item -Path $InstallLocation -ItemType Directory
}

$ExclusionPath = "C:\Tools\metasploit-framework"

try {
	Add-MpPreference -ExclusionPath $ExclusionPath
	Write-Host "Windows Defender exclusion added for $ExclusionPath"
	Write-Host "THIS IS DONE TO PREVENT WINDOWS DEFENDER FROM DELETING METASPLOIT FILES."
} catch {
	Write-Host "Error adding Windows Defender exclusion: $_"
}

# Set the installer path
$Installer = "$DownloadLocation/metasploit.msi"

# Download Metasploit installer
Invoke-WebRequest -UseBasicParsing -Uri $DownloadURL -OutFile $Installer

# Install Metasploit
& $Installer /q /log $LogLocation INSTALLLOCATION="$InstallLocation"
