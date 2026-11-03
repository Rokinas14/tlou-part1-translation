# Copy a patched core.psarc into the game, with the checks that matter.
#
#   powershell -File tools\swap_in.ps1 -Patched "E:\tlou\core_translated.psarc" `
#       -Backup "E:\tlou\core_pristine.psarc"
#
# Refuses to run while the game is open, and refuses a backup that has changed
# since the first run (it stores the backup's md5 next to it in <backup>.md5).
param(
    [Parameter(Mandatory = $true)][string]$Patched,
    [Parameter(Mandatory = $true)][string]$Backup,
    [string]$Game = 'D:\SteamLibrary\steamapps\common\The Last of Us Part I'
)
$ErrorActionPreference = 'Stop'

$core = Join-Path $Game 'build\pc\main\core.psarc'
$main = Split-Path $core -Parent

if (-not (Test-Path $Game)) { throw "Game folder not found: $Game" }
if (-not (Test-Path $core)) { throw "core.psarc not found: $core" }
if (-not (Test-Path $Backup)) { throw "Pristine backup missing: $Backup" }
if (-not (Test-Path $Patched)) { throw "Patched archive not found: $Patched" }

$proc = Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -like 'tlou*' }
if ($proc) { throw "Game is running ($($proc.ProcessName -join ', ')) - close it first, nothing was changed." }

# the backup must be the same file we checked the first time
$stamp = "$Backup.md5"
$backupMd5 = (Get-FileHash -Algorithm MD5 -LiteralPath $Backup).Hash.ToLower()
if (Test-Path $stamp) {
    $known = (Get-Content $stamp -Raw).Trim().ToLower()
    if ($known -ne $backupMd5) { throw "Backup changed since last time ($backupMd5 vs $known) - refusing." }
    "backup verified: $backupMd5"
} else {
    Set-Content -LiteralPath $stamp -Value $backupMd5 -NoNewline
    "backup recorded: $backupMd5"
}

"patched file: {0:N0} bytes" -f (Get-Item -LiteralPath $Patched).Length

# free the space first: the drive holds one archive, not two
$liveMd5 = (Get-FileHash -Algorithm MD5 -LiteralPath $core).Hash.ToLower()
if ($liveMd5 -eq $backupMd5) { "the live archive was still the original" }
else { "the live archive was a previous patch, it is replaced" }
Remove-Item -LiteralPath $core -Force
"removed the live archive to free space"

Copy-Item -LiteralPath $Patched -Destination $core -Force
$h1 = (Get-FileHash -Algorithm MD5 -LiteralPath $Patched).Hash
$h2 = (Get-FileHash -Algorithm MD5 -LiteralPath $core).Hash
if ($h1 -ne $h2) { throw "Copy mismatch after writing: $h1 vs $h2" }

"installed md5 $h2  match: True"
"In game: Options -> Text Language -> your language."
"To undo: Steam -> Properties -> Installed Files -> Verify integrity of game files."
