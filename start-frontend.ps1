# Frontend Startup Script
Write-Host "Starting Frontend Server..." -ForegroundColor Green

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org/" -ForegroundColor Yellow
    Write-Host "After installation, RESTART PowerShell and try again" -ForegroundColor Yellow
    exit 1
}

# Navigate to frontend directory
if (-not (Test-Path "frontend")) {
    Write-Host "ERROR: frontend directory not found" -ForegroundColor Red
    Write-Host "Make sure you're in the project root directory" -ForegroundColor Red
    exit 1
}

Set-Location frontend

# Check if dependencies are installed
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}

# Start development server
Write-Host "Starting Vite development server on http://localhost:3000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

npm run dev

