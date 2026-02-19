# Backend - Pneumonia Detection System

## Overview

FastAPI-based backend for pneumonia detection and classification using deep learning models.

## Architecture

### Core Components

1. **FastAPI Application** (`main.py`)
   - Startup: Loads all ML models
   - Lifespan management
   - Route registration
   - CORS configuration

2. **API Endpoints** (`api/`)
   - `auth.py` - User registration, login, JWT tokens
   - `inference.py` - Complete prediction pipeline
   - `users.py` - Profile management, scan history

3. **ML Services** (`services/`)
   - `segmentation_service.py` - U-Net lung segmentation
   - `stage1_classifier.py` - Binary classification
   - `stage2_classifier.py` - Viral vs Bacterial classification
   - `preprocessing.py` - Image preprocessing

4. **Database** (`db/`)
   - MongoDB async connection
   - Pydantic schemas for validation
   - User and scan history collections

5. **Core** (`core/`)
   - Configuration management
   - JWT security utilities
   - Password hashing

## Model Loading

### U-Net Segmentation (CRITICAL)
```python
# DOES NOT use keras.models.load_model()
# Reconstructs architecture from config.json
# Loads weights from model.weights.h5
```

**Files required:**
- `models/lung_segmentation/config.json`
- `models/lung_segmentation/model.weights.h5`
- `models/lung_segmentation/metadata.json`

### Stage-1 Classifier
```python
# Single .keras file
model = keras.models.load_model('stage1_convnext.keras')
```

### Stage-2 Classifier
```python
# Single .keras file with dual inputs
model = keras.models.load_model('dual_input_stage2_final.keras')
```

## Prediction Pipeline

1. **Validate uploaded image**
   - Check file type (JPEG, PNG)
   - Validate file size (<10MB)
   - Verify image integrity

2. **Preprocess**
   - Convert to grayscale
   - Resize to 224×224
   - Normalize to [0, 1]

3. **Lung Segmentation**
   - U-Net prediction
   - Mask postprocessing
   - Morphological operations

4. **Stage-1: Binary Classification**
   - ConvNeXt preprocessing
   - Normal vs Pneumonia prediction
   - Confidence scoring

5. **Stage-2: Pneumonia Classification** (if needed)
   - Dual-input (original + segmented)
   - Viral vs Bacterial prediction
   - Final confidence scoring

6. **Response Formatting**
   - Convert images to base64
   - Add medical disclaimer
   - Save to scan history

## Configuration

### Environment Variables (.env)
```env
SECRET_KEY=your-secret-key-min-32-chars
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=pneumonia_detection
HOST=0.0.0.0
PORT=8000
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Important Settings
- Image size: 224×224
- Max file size: 10MB
- Stage-1 threshold: 0.5
- Stage-2 threshold: 0.5

## API Authentication

All prediction and user endpoints require JWT authentication:

```http
Authorization: Bearer <token>
```

Token obtained from `/api/v1/auth/login` or `/api/v1/auth/signup`

## Database Schema

### Users Collection
```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "hashed_password": "...",
  "full_name": "John Doe",
  "created_at": ISODate,
  "is_active": true
}
```

### Scan History Collection
```json
{
  "_id": ObjectId,
  "user_id": "user_id_string",
  "prediction_label": "Normal",
  "confidence": 0.95,
  "stage": 1,
  "created_at": ISODate
}
```

## Running the Backend

### Development
```powershell
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```powershell
cd app
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Testing Endpoints

### Using Swagger UI
Navigate to: `http://localhost:8000/docs`

### Using curl
```powershell
# Health check
curl http://localhost:8000/health

# Signup
curl -X POST http://localhost:8000/api/v1/auth/signup `
  -H "Content-Type: application/json" `
  -d '{"email":"test@example.com","password":"Test1234","full_name":"Test User"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{"email":"test@example.com","password":"Test1234"}'
```

## Error Handling

All errors return consistent format:
```json
{
  "success": false,
  "message": "Error description",
  "error_code": "OPTIONAL_CODE",
  "timestamp": "2024-01-01T00:00:00"
}
```

## Performance Considerations

- Models loaded once at startup (not per request)
- Async MongoDB operations
- Image preprocessing optimized for CPU
- Response caching not implemented (stateless)

## Security

- Bcrypt password hashing
- JWT with expiration
- CORS restricted to frontend origins
- Input validation on all endpoints
- File upload size limits

## Logging

Structured logging at INFO level:
- Model loading status
- Request processing
- Errors with stack traces
- Authentication events

## Troubleshooting

**Model Loading Failures:**
- Check file paths in `core/config.py`
- Verify model files exist
- Check TensorFlow/Keras compatibility

**MongoDB Connection Issues:**
- Verify MongoDB is running
- Check connection string
- Test with MongoDB Compass

**Import Errors:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**Performance Issues:**
- Models are CPU-optimized
- Consider GPU for production
- Adjust batch size if needed
