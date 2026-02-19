# Two-Stage Explainable Pneumonia Detection and Classification System

A production-ready, medical-grade web application for detecting and classifying pneumonia in chest X-ray images using deep learning.

## 🎯 Project Overview

This system performs:
1. **Lung Segmentation** - Isolates lung regions using U-Net
2. **Binary Classification** - Normal vs Pneumonia detection using ConvNeXt
3. **Secondary Classification** - Viral vs Bacterial Pneumonia using dual-input ConvNeXt

## 🏗️ Technology Stack

### Backend
- **Framework:** FastAPI (Python 3.10+)
- **ML/AI:** TensorFlow/Keras, OpenCV, Pillow
- **Database:** MongoDB (PyMongo/Motor)
- **Authentication:** JWT (python-jose)
- **Server:** Uvicorn

### Frontend
- **Framework:** React 18 + Vite
- **Styling:** TailwindCSS
- **HTTP Client:** Axios
- **Routing:** React Router v6
- **Icons:** Lucide React

## 📂 Project Structure

```
pneumonia-detection-system/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application
│   │   ├── api/                    # API endpoints
│   │   │   ├── auth.py            # Authentication
│   │   │   ├── inference.py       # Prediction pipeline
│   │   │   └── users.py           # User management
│   │   ├── core/                  # Core configuration
│   │   │   ├── config.py          # Settings
│   │   │   └── security.py        # JWT & password hashing
│   │   ├── models/                # Model files
│   │   │   ├── lung_segmentation/ # U-Net model files
│   │   │   ├── stage1_convnext.keras
│   │   │   └── dual_input_stage2_final.keras
│   │   ├── services/              # ML services
│   │   │   ├── preprocessing.py
│   │   │   ├── segmentation_service.py
│   │   │   ├── stage1_classifier.py
│   │   │   └── stage2_classifier.py
│   │   ├── db/                    # Database
│   │   │   ├── mongodb.py
│   │   │   └── schemas.py
│   │   └── utils/                 # Utilities
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/            # React components
│   │   ├── pages/                 # Page components
│   │   ├── services/              # API service
│   │   ├── context/               # Auth context
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── .env.example
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- MongoDB 5.0 or higher
- Git

### Backend Setup

1. **Navigate to backend directory:**
   ```powershell
   cd backend
   ```

2. **Create virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Place model files:**
   - Copy your trained model files to `app/models/`:
     - `lung_segmentation/model.weights.h5`
     - `lung_segmentation/config.json`
     - `lung_segmentation/metadata.json`
     - `stage1_convnext.keras`
     - `dual_input_stage2_final.keras`

5. **Configure environment:**
   ```powershell
   copy .env.example .env
   ```
   Edit `.env` and set:
   - `SECRET_KEY` - Strong random key (min 32 chars)
   - `MONGODB_URL` - Your MongoDB connection string
   - Other settings as needed

6. **Start MongoDB:**
   ```powershell
   # If using local MongoDB
   mongod
   ```

7. **Run the backend:**
   ```powershell
   cd app
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at: `http://localhost:8000`
   API Documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```powershell
   cd frontend
   ```

2. **Install dependencies:**
   ```powershell
   npm install
   ```

3. **Configure environment:**
   ```powershell
   copy .env.example .env
   ```

4. **Start development server:**
   ```powershell
   npm run dev
   ```

   Frontend will be available at: `http://localhost:3000`

## 🧪 Testing the System

1. **Register a new account** at `http://localhost:3000/signup`
2. **Login** with your credentials
3. **Upload a chest X-ray** from the dashboard
4. **View results** with predictions and segmentation

## 🔒 Security Features

- **Password Hashing:** Bcrypt with salt
- **JWT Authentication:** Secure token-based auth
- **Input Validation:** Pydantic schemas
- **File Validation:** Type and size checks
- **CORS Protection:** Configured allowed origins

## 🎯 Model Pipeline

### Stage 1: Lung Segmentation
- **Architecture:** U-Net
- **Input:** 224×224 grayscale
- **Output:** Binary lung mask
- **Purpose:** Isolate lung regions

### Stage 2: Binary Classification
- **Architecture:** ConvNeXt
- **Input:** 224×224 RGB (from grayscale)
- **Output:** Normal vs Pneumonia
- **Threshold:** 0.5 (configurable)

### Stage 3: Pneumonia Classification
- **Architecture:** Dual-input ConvNeXt
- **Input 1:** Original X-ray (224×224)
- **Input 2:** Segmented lung (224×224)
- **Output:** Viral vs Bacterial
- **Executes:** Only if Stage 2 detects pneumonia

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/login` - Login user

### Inference
- `POST /api/v1/inference/predict` - Analyze X-ray
- `GET /api/v1/inference/models/status` - Model status
- `GET /api/v1/inference/health` - Health check

### Users
- `GET /api/v1/users/me` - Get user profile
- `PUT /api/v1/users/me` - Update profile
- `POST /api/v1/users/change-password` - Change password
- `GET /api/v1/users/history` - Get scan history

## ⚠️ Important Notes

### Model Files
- **DO NOT** rename model files
- **DO NOT** modify model architectures
- Models are loaded once at startup
- Ensure all model files exist before starting backend

### Medical Disclaimer
**This system is for research and educational purposes only. DO NOT use for clinical diagnosis. Always consult qualified healthcare professionals.**

## 🐛 Troubleshooting

### Backend Issues

**Models not loading:**
- Verify all model files are in correct locations
- Check file permissions
- Review logs for specific errors

**MongoDB connection failed:**
- Ensure MongoDB is running
- Check connection string in `.env`
- Verify network access

**Import errors:**
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

### Frontend Issues

**API connection failed:**
- Verify backend is running
- Check `VITE_API_URL` in `.env`
- Review browser console for CORS errors

**Build errors:**
- Delete `node_modules` and reinstall: `npm install`
- Clear cache: `npm cache clean --force`

## 📝 Development

### Backend Development
```powershell
cd backend/app
python -m uvicorn main:app --reload
```

### Frontend Development
```powershell
cd frontend
npm run dev
```

### Production Build

**Backend:**
```powershell
cd backend/app
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```powershell
cd frontend
npm run build
npm run preview
```

## 📄 License

This project is for educational and research purposes.

## 👥 Support

For issues and questions:
1. Check documentation in `backend/app/models/README.md`
2. Review API docs at `/docs`
3. Check troubleshooting section above

## 🎓 Acknowledgments

- U-Net for medical image segmentation
- ConvNeXt for state-of-the-art classification
- FastAPI for modern Python web framework
- React for responsive UI development
