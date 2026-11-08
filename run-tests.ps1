# PowerShell Test Runner for CyberShield AI Master Project
$ErrorActionPreference = "Stop"

$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

# Determine Python Executable
$PythonExe = "D:\My Created Projects\ai hackathon\.venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    $PythonExe = "python.exe"
}

$env:PYTHONPATH = $ProjectRoot
$env:PYTHONIOENCODING = "utf-8"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " CyberShield AI - Executing Master Test Suite" -ForegroundColor Cyan
Write-Host " Python: $PythonExe" -ForegroundColor DarkGray
Write-Host "============================================================" -ForegroundColor Cyan

& $PythonExe -m pytest tests/ -v

Write-Host "`nTest execution completed successfully!" -ForegroundColor Green
