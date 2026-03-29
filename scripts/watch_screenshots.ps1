# watch_screenshots.ps1
# Watches the Windows Screenshots folder and copies new files
# to a project-local folder so Claude Code can access them.

$SOURCE  = "C:\Users\Geoff\Pictures\Screenshots"
$DEST    = "C:\Dev\ClaudeCreator\Screenshots"

$PID_DIR  = Join-Path $DEST ".pids"
$PID_FILE = Join-Path $PID_DIR "screenshot_watcher.pid"

if (-not (Test-Path $DEST))    { New-Item -ItemType Directory -Force -Path $DEST    | Out-Null }
if (-not (Test-Path $PID_DIR)) { New-Item -ItemType Directory -Force -Path $PID_DIR | Out-Null }

[System.IO.File]::WriteAllText($PID_FILE, "$PID", [System.Text.Encoding]::ASCII)

Write-Host "[screenshot-watcher] pid=$PID  source=$SOURCE"

while ($true) {
    try {
        $watcher = New-Object System.IO.FileSystemWatcher
        $watcher.Path                  = $SOURCE
        $watcher.Filter                = "*.*"
        $watcher.IncludeSubdirectories = $false
        $watcher.EnableRaisingEvents   = $true

        $action = {
            $file = $Event.SourceEventArgs.FullPath
            $name = $Event.SourceEventArgs.Name
            $dest = $Event.MessageData
            Start-Sleep -Milliseconds 500
            try {
                $dst = Join-Path $dest $name
                Copy-Item -LiteralPath $file -Destination $dst -Force
                Write-Host "[screenshot-watcher] copied: $name"
            } catch {
                Write-Host "[screenshot-watcher] error copying ${name}: $_"
            }
        }

        $createdJob = Register-ObjectEvent -InputObject $watcher -EventName Created -Action $action -MessageData $DEST
        $renamedJob = Register-ObjectEvent -InputObject $watcher -EventName Renamed -Action $action -MessageData $DEST

        Write-Host "[screenshot-watcher] watching..."
        while ($true) { Start-Sleep 5 }
    } catch {
        Write-Host "[screenshot-watcher] error: $_ -- restarting in 5s"
    } finally {
        try { Unregister-Event -SourceIdentifier $createdJob.Name -ErrorAction SilentlyContinue } catch {}
        try { Unregister-Event -SourceIdentifier $renamedJob.Name -ErrorAction SilentlyContinue } catch {}
        try { $watcher.Dispose() } catch {}
    }
    Start-Sleep 5
}
