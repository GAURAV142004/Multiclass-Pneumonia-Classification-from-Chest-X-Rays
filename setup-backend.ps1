# Backend Setup Script
# Automates backend setup process

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Backend Setup - Pneumonia Detection System" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to backend
Set-Location -Path "backend"

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies (this may take a few minutes)..." -ForegroundColor Yellow
pip install -r requirements.txt

# Setup .env if not exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "IMPORTANT: Edit backend/.env and set a secure SECRET_KEY!" -ForegroundColor Red
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Backend setup complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit backend/.env and set SECRET_KEY" -ForegroundColor White
Write-Host "2. Ensure MongoDB is running" -ForegroundColor White
Write-Host "3. Place model files in backend/app/models/" -ForegroundColor White
Write-Host "4. Run backend:" -ForegroundColor White
Write-Host "   cd app" -ForegroundColor Cyan
Write-Host "   python -m uvicorn main:app --reload" -ForegroundColor Cyan
Write-Host ""

Set-Location -Path ".."
