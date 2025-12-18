# Start Both Backend and Frontend
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Geo-fencing Platform - Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Node.js not found. Frontend will not start." -ForegroundColor Yellow
    Write-Host "Install from https://nodejs.org/ and restart PowerShell" -ForegroundColor Yellow
    Write-Host ""
}

# Start Backend in new window
Write-Host "Starting Backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\start-backend.ps1"

# Wait a bit
Start-Sleep -Seconds 2

# Start Frontend in new window
Write-Host "Starting Frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\start-frontend.ps1"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Services Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host "API Docs: http://localhost:8000/api/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Two PowerShell windows will open - one for each service" -ForegroundColor Yellow
Write-Host "Close those windows to stop the services" -ForegroundColor Yellow

