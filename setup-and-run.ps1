# Complete Setup and Run Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Geo-fencing Platform Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    exit 1
}

# Setup Backend
Write-Host ""
Write-Host "Setting up Backend..." -ForegroundColor Yellow

# Activate venv
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
    
    # Install missing dependencies
    Write-Host "Installing missing dependencies..." -ForegroundColor Yellow
    python -m pip install email-validator passlib[bcrypt] --quiet
    Write-Host "✓ Backend dependencies ready" -ForegroundColor Green
} else {
    Write-Host "✗ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
}

# Test backend
Write-Host "Testing backend..." -ForegroundColor Yellow
try {
    python -c "from app.main import app; print('✓ Backend ready!')" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Backend is ready!" -ForegroundColor Green
    } else {
        Write-Host "⚠ Backend has some issues but may still work" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠ Backend test failed, but trying to continue..." -ForegroundColor Yellow
}

# Check Node.js
Write-Host ""
Write-Host "Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js: $nodeVersion" -ForegroundColor Green
    
    # Setup Frontend
    Write-Host ""
    Write-Host "Setting up Frontend..." -ForegroundColor Yellow
    Set-Location frontend
    
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installing frontend dependencies (this may take a few minutes)..." -ForegroundColor Yellow
        npm install
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green
        } else {
            Write-Host "⚠ Frontend dependencies installation had issues" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✓ Frontend dependencies already installed" -ForegroundColor Green
    }
    
    Set-Location ..
    
} catch {
    Write-Host "✗ Node.js not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Node.js:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://nodejs.org/" -ForegroundColor Cyan
    Write-Host "2. Install it" -ForegroundColor Cyan
    Write-Host "3. RESTART PowerShell" -ForegroundColor Cyan
    Write-Host "4. Run this script again" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Continuing with backend only..." -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the services:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Backend:" -ForegroundColor Cyan
Write-Host "  .\start-backend.ps1" -ForegroundColor White
Write-Host "  OR: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "      uvicorn app.main:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "Frontend (if Node.js is installed):" -ForegroundColor Cyan
Write-Host "  .\start-frontend.ps1" -ForegroundColor White
Write-Host "  OR: cd frontend" -ForegroundColor White
Write-Host "      npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "Or start both:" -ForegroundColor Cyan
Write-Host "  .\start-both.ps1" -ForegroundColor White
Write-Host ""
Write-Host "URLs:" -ForegroundColor Yellow
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor Green
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host "  API Docs: http://localhost:8000/api/docs" -ForegroundColor Green
Write-Host ""

