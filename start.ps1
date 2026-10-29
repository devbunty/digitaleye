# Start Digital Eye (backend + dashboard) on Windows.
# Usage:  .\start.ps1      (or double-click start.bat)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv .venv
}

Write-Host "Installing backend dependencies..."
& .\.venv\Scripts\python.exe -m pip install -q -r requirements.txt

if (-not (Test-Path "dashboard\frontend\node_modules")) {
    Write-Host "Installing dashboard dependencies (first run only)..."
    npm --prefix dashboard/frontend install
}

# Backend in its own window so both stay visible.
$root = $PSScriptRoot
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$root'; .\.venv\Scripts\python.exe run.py"

Write-Host ""
Write-Host "Backend : http://localhost:5000"
Write-Host "Dashboard: http://localhost:5173  (starting...)"
Write-Host ""
npm --prefix dashboard/frontend run dev
