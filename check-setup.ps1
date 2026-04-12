# Pneumonia Detection System - Setup Script
# Run this script to check prerequisites and guide setup

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Pneumonia Detection System - Setup Checker" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check Python
Write-Host "Checking Python..." -NoNewline
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.([0-9]+)") {
        $minorVersion = [int]$Matches[1]
        if ($minorVersion -ge 10) {
            Write-Host " OK ($pythonVersion)" -ForegroundColor Green
        } else {
            Write-Host " ERROR: Python 3.10+ required (found $pythonVersion)" -ForegroundColor Red
            $allGood = $false
        }
    }
} catch {
    Write-Host " ERROR: Python not found" -ForegroundColor Red
    $allGood = $false
}

# Check Node.js
Write-Host "Checking Node.js..." -NoNewline
try {
    $nodeVersion = node --version 2>&1
    if ($nodeVersion -match "v([0-9]+)") {
        $majorVersion = [int]$Matches[1]
        if ($majorVersion -ge 18) {
            Write-Host " OK ($nodeVersion)" -ForegroundColor Green
        } else {
            Write-Host " ERROR: Node.js 18+ required (found $nodeVersion)" -ForegroundColor Red
            $allGood = $false
        }
    }
} catch {
    Write-Host " ERROR: Node.js not found" -ForegroundColor Red
    $allGood = $false
}

# Check npm
Write-Host "Checking npm..." -NoNewline
try {
    $npmVersion = npm --version 2>&1
    Write-Host " OK ($npmVersion)" -ForegroundColor Green
} catch {
    Write-Host " ERROR: npm not found" -ForegroundColor Red
    $allGood = $false
}

# Check MongoDB
Write-Host "Checking MongoDB..." -NoNewline
try {
    $mongoVersion = mongod --version 2>&1
    if ($mongoVersion -match "v([0-9]+)") {
        Write-Host " OK" -ForegroundColor Green
    }
} catch {
    Write-Host " WARNING: MongoDB not found (you can use MongoDB Atlas)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Directory Structure Check" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Check backend structure
Write-Host "Checking backend structure..." -NoNewline
$backendExists = Test-Path ".\backend\app\main.py"
if ($backendExists) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " ERROR: Backend structure incomplete" -ForegroundColor Red
    $allGood = $false
}

# Check frontend structure
Write-Host "Checking frontend structure..." -NoNewline
$frontendExists = Test-Path ".\frontend\package.json"
if ($frontendExists) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " ERROR: Frontend structure incomplete" -ForegroundColor Red
    $allGood = $false
}

# Check model directory
Write-Host "Checking model directory..." -NoNewline
$modelDirExists = Test-Path ".\backend\app\models"
if ($modelDirExists) {
    Write-Host " OK" -ForegroundColor Green
    
    # Check for model files
    Write-Host "  Checking model files..."
    $hasSegWeights = Test-Path ".\backend\app\models\lung_segmentation\model.weights.h5"
    $hasStage1 = Test-Path ".\backend\app\models\stage1_convnext.keras"
    $hasStage2 = Test-Path ".\backend\app\models\dual_input_stage2_final.keras"
    
    if (-not $hasSegWeights) {
        Write-Host "    - lung_segmentation/model.weights.h5" -NoNewline
        Write-Host " MISSING" -ForegroundColor Yellow
    } else {
        Write-Host "    - lung_segmentation/model.weights.h5" -NoNewline
        Write-Host " OK" -ForegroundColor Green
    }
    
    if (-not $hasStage1) {
        Write-Host "    - stage1_convnext.keras" -NoNewline
        Write-Host " MISSING" -ForegroundColor Yellow
    } else {
        Write-Host "    - stage1_convnext.keras" -NoNewline
        Write-Host " OK" -ForegroundColor Green
    }
    
    if (-not $hasStage2) {
        Write-Host "    - dual_input_stage2_final.keras" -NoNewline
        Write-Host " MISSING" -ForegroundColor Yellow
    } else {
        Write-Host "    - dual_input_stage2_final.keras" -NoNewline
        Write-Host " OK" -ForegroundColor Green
    }
} else {
    Write-Host " ERROR: Model directory not found" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Environment Configuration" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Check backend .env
Write-Host "Checking backend .env..." -NoNewline
$backendEnvExists = Test-Path ".\backend\.env"
if ($backendEnvExists) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " MISSING (run: copy backend\.env.example backend\.env)" -ForegroundColor Yellow
}

# Check frontend .env
Write-Host "Checking frontend .env..." -NoNewline
$frontendEnvExists = Test-Path ".\frontend\.env"
if ($frontendEnvExists) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " MISSING (run: copy frontend\.env.example frontend\.env)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "All prerequisites met!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Place your trained model files in backend/app/models/" -ForegroundColor White
    Write-Host "2. Configure .env files (copy from .env.example)" -ForegroundColor White
    Write-Host "3. Run: " -NoNewline -ForegroundColor White
    Write-Host ".\setup-backend.ps1" -ForegroundColor Yellow
    Write-Host "4. Run: " -NoNewline -ForegroundColor White
    Write-Host ".\setup-frontend.ps1" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or see SETUP.md for detailed instructions" -ForegroundColor Cyan
} else {
    Write-Host "Some prerequisites are missing. Please install required software." -ForegroundColor Red
    Write-Host ""
    Write-Host "Required:" -ForegroundColor Cyan
    Write-Host "- Python 3.10+" -ForegroundColor White
    Write-Host "- Node.js 18+" -ForegroundColor White
    Write-Host "- MongoDB (or MongoDB Atlas)" -ForegroundColor White
}

Write-Host ""
