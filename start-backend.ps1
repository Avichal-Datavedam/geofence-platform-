# Backend Startup Script
Write-Host "Starting Backend Server..." -ForegroundColor Green

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Check if activation worked
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Could not activate virtual environment" -ForegroundColor Red
    Write-Host "Make sure you're in the project root directory" -ForegroundColor Red
    exit 1
}

# Start server
Write-Host "Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
Write-Host "API Docs: http://localhost:8000/api/docs" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

uvicorn app.main:app --reload --port 8000

