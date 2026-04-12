# Quick Setup Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Setup Backend (2 minutes)

```powershell
# Navigate to backend
cd "C:\Users\dell\Downloads\Major Project\backend"

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env
# Edit .env and change SECRET_KEY to a secure random string
```

### Step 2: Add Your Model Files

Place your trained models in `backend/app/models/`:
- `lung_segmentation/model.weights.h5`
- `lung_segmentation/config.json` (already exists - update if needed)
- `lung_segmentation/metadata.json` (already exists - update if needed)
- `stage1_convnext.keras`
- `dual_input_stage2_final.keras`

### Step 3: Start MongoDB

```powershell
# If MongoDB is not running, start it
mongod
```

Or use MongoDB Atlas cloud connection (update MONGODB_URL in .env)

### Step 4: Start Backend (1 minute)

```powershell
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend running at: http://localhost:8000
📚 API Docs at: http://localhost:8000/docs

### Step 5: Setup Frontend (2 minutes)

Open a NEW terminal:

```powershell
# Navigate to frontend
cd "C:\Users\dell\Downloads\Major Project\frontend"

# Install dependencies
npm install

# Setup environment
copy .env.example .env

# Start frontend
npm run dev
```

✅ Frontend running at: http://localhost:3000

## 🎉 You're Ready!

1. Open browser: http://localhost:3000
2. Sign up for an account
3. Upload a chest X-ray
4. View results!

## 📋 Pre-Flight Checklist

Before running:
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] MongoDB running or connection string ready
- [ ] Model files placed in correct directories
- [ ] .env files configured
- [ ] Virtual environment activated (backend)

## ⚠️ Common Issues

**Backend won't start:**
- Check if MongoDB is running
- Verify model files exist
- Ensure virtual environment is activated

**Frontend won't start:**
- Run `npm install` again
- Delete `node_modules` and reinstall
- Check port 3000 is available

**CORS errors:**
- Backend and frontend must be running
- Check ALLOWED_ORIGINS in backend config.py

## 🔧 Development URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- MongoDB: mongodb://localhost:27017

## 📖 Next Steps

1. Read [README.md](README.md) for detailed information
2. Check [backend/README.md](backend/README.md) for API details
3. Check [frontend/README.md](frontend/README.md) for UI details
4. Review [backend/app/models/README.md](backend/app/models/README.md) for model requirements

## 🆘 Need Help?

1. Check the main README.md troubleshooting section
2. Review API docs at /docs
3. Check browser console for frontend errors
4. Check terminal logs for backend errors

## 🎯 Production Deployment

For production deployment:
1. Change DEBUG=False in backend .env
2. Set strong SECRET_KEY (32+ characters)
3. Use production MongoDB instance
4. Build frontend: `npm run build`
5. Use proper web server (Nginx, Apache)
6. Enable HTTPS
7. Set secure CORS origins

---

**Medical Disclaimer:** This system is for research and educational purposes only. Always consult qualified healthcare professionals for medical diagnosis.
