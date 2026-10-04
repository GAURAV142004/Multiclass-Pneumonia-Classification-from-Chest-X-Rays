# 🫁 Two-Stage Explainable Pneumonia Detection & Classification

> A research/educational prototype combining medical-image segmentation, deep-learning classification, a FastAPI backend and a React frontend into an end-to-end ML application.

<p align="center">
  <img src="https://img.shields.io/badge/ML-Computer%20Vision-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react" />
  <img src="https://img.shields.io/badge/Database-MongoDB-47A248?style=for-the-badge&logo=mongodb" />
</p>

---

## 🎯 Project Overview

The system explores a staged computer-vision pipeline for chest X-ray analysis:

```text
Chest X-ray
    ↓
Lung Segmentation
    │  U-Net
    ↓
Normal vs Pneumonia
    │  ConvNeXt
    ↓
Viral vs Bacterial
    │  Dual-input ConvNeXt
    ↓
Prediction + Segmentation Result
```

### Pipeline

1. **Lung segmentation** — isolates lung regions using U-Net.
2. **Binary classification** — distinguishes normal X-rays from pneumonia cases using ConvNeXt.
3. **Secondary classification** — attempts viral vs bacterial classification using a dual-input ConvNeXt model.

The staged approach is intended to explore how preprocessing and segmentation can be incorporated into an end-to-end inference pipeline.

---

## 🏗️ Architecture

```text
┌─────────────────────┐
│     React / Vite    │
│     Web Frontend    │
└──────────┬──────────┘
           │ HTTP
           ▼
┌─────────────────────┐
│       FastAPI       │
│ Authentication/API  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Inference Service │
│                     │
│ U-Net → ConvNeXt    │
│       → ConvNeXt    │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
  MongoDB     ML Models
```

---

## 🛠️ Technology Stack

### Backend

- Python 3.10+
- FastAPI
- TensorFlow / Keras
- OpenCV
- Pillow
- MongoDB / PyMongo / Motor
- JWT authentication
- Uvicorn

### Frontend

- React 18
- Vite
- Tailwind CSS
- Axios
- React Router
- Lucide React

### ML

- U-Net
- ConvNeXt
- Image preprocessing
- Segmentation masks
- Multi-stage inference

---

## 📂 Project Structure

```text
pneumonia-detection-system/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   ├── db/
│   │   └── utils/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── context/
│   └── package.json
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB 5+
- Git

### Backend

```bash
cd backend
python -m venv venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` from `.env.example` and configure the required MongoDB and authentication settings.

Run the API:

```bash
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API documentation is available at:

```text
http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔌 API Surface

### Authentication

```text
POST /api/v1/auth/signup
POST /api/v1/auth/login
```

### Inference

```text
POST /api/v1/inference/predict
GET  /api/v1/inference/models/status
GET  /api/v1/inference/health
```

### Users

```text
GET  /api/v1/users/me
PUT  /api/v1/users/me
POST /api/v1/users/change-password
GET  /api/v1/users/history
```

---

## 🔐 Engineering & Security

The application includes:

- JWT-based authentication
- Password hashing
- Pydantic validation
- Upload type/size validation
- CORS configuration
- Environment-based secrets
- Model loading at application startup

---

## ⚠️ Medical Disclaimer

**This project is for research and educational purposes only. It is not a medical device and must not be used for clinical diagnosis or treatment decisions.**

The model predictions should not be interpreted as medical advice. Qualified healthcare professionals and appropriately validated clinical systems must be used for real-world diagnosis.

---

## 🧪 What This Project Demonstrates

This project was valuable because it combines multiple engineering layers rather than treating machine learning as an isolated notebook:

- Model inference
- Image preprocessing
- Segmentation
- Classification
- REST API design
- Authentication
- Database integration
- React frontend development
- End-to-end application architecture

---

## 📌 Project Status

**Status:** Research / educational prototype.

The repository is preserved as part of my transition from traditional software development toward **AI and applied machine learning engineering**.

---

## 👨‍💻 Author

**Gaurav Rajendra Pawar**  
Software Developer · AI & Cloud Engineering

- GitHub: https://github.com/GAURAV142004
- LinkedIn: https://linkedin.com/in/gaurav-pawar-277555257
