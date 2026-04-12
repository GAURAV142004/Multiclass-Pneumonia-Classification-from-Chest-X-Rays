# Frontend Setup Script
# Automates frontend setup process

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Frontend Setup - Pneumonia Detection System" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend
Set-Location -Path "frontend"

# Install dependencies
Write-Host "Installing Node.js dependencies (this may take a few minutes)..." -ForegroundColor Yellow
npm install

# Setup .env if not exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Frontend setup complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Ensure backend is running on port 8000" -ForegroundColor White
Write-Host "2. Run frontend:" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor Cyan
Write-Host ""
Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor Green
Write-Host ""

Set-Location -Path ".."
