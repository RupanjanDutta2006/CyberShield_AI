# PowerShell Server Runner for CyberShield AI Master Project
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
Write-Host " CyberShield AI - Launching Full-Stack Platform" -ForegroundColor Cyan
Write-Host " Serving FastAPI Backend + React UI on http://localhost:8000" -ForegroundColor Green
Write-Host " API Docs available at http://localhost:8000/docs" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

& $PythonExe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
