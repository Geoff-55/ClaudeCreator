# Mark — launch the local routing CLI from the current directory
param([string]$Dir = (Get-Location).Path)
& "C:/Users/Geoff/AppData/Local/Programs/Python/Python312/python.exe" `
    "C:/Dev/ClaudeCreator/scripts/mark.py" --dir $Dir
