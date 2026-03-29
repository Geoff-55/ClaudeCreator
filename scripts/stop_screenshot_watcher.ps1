# stop_screenshot_watcher.ps1
$PID_FILE = "C:\Dev\ClaudeCreator\Screenshots\.pids\screenshot_watcher.pid"

if (-not (Test-Path $PID_FILE)) {
    Write-Host "[screenshot-watcher] not running (no pid file)"
    return
}

$raw = [System.IO.File]::ReadAllText($PID_FILE).Trim()
try { $procId = [int]::Parse($raw) } catch { Write-Host "[screenshot-watcher] bad pid file: $raw"; return }

$proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
if ($proc) {
    Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
    Write-Host "[screenshot-watcher] stopped pid=$procId"
} else {
    Write-Host "[screenshot-watcher] pid=$procId already exited"
}

Remove-Item $PID_FILE -Force -ErrorAction SilentlyContinue
