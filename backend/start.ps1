# Start Backend Server from backend directory
# Run this script from: C:\Users\dell\Downloads\Major Project\backend

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Starting Pneumonia Detection Backend" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the correct directory
if (-not (Test-Path ".\app\main.py")) {
    Write-Host "ERROR: Please run this script from the backend directory" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    Write-Host "Expected: backend folder containing app\ subdirectory" -ForegroundColor Yellow
    exit 1
}

# Check if .env exists
if (-not (Test-Path ".\.env")) {
    Write-Host "WARNING: .env file not found. Creating from .env.example..." -ForegroundColor Yellow
    if (Test-Path ".\.env.example") {
        Copy-Item ".\.env.example" ".\.env"
        Write-Host "IMPORTANT: Edit .env and set SECRET_KEY before proceeding!" -ForegroundColor Red
        Write-Host ""
        pause
    } else {
        Write-Host "ERROR: .env.example not found!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Starting Uvicorn server..." -ForegroundColor Yellow
Write-Host ""

# Run uvicorn from backend directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
