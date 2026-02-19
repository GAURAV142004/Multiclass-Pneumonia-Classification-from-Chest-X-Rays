# Model Files Directory

## Required Model Files

Place your trained model files in this directory:

### 1. Lung Segmentation Model (U-Net)
**Directory:** `lung_segmentation/`
- `model.weights.h5` - Pre-trained U-Net weights
- `config.json` - Model architecture configuration
- `metadata.json` - Model metadata and preprocessing info

### 2. Stage-1 Binary Classifier
**File:** `stage1_convnext.keras`
- ConvNeXt-based binary classifier
- Classifies: Normal vs Pneumonia
- Input: 224x224x3 RGB image
- Output: Sigmoid probability

### 3. Stage-2 Dual-Input Classifier
**File:** `dual_input_stage2_final.keras`
- Dual-input ConvNeXt classifier
- Classifies: Viral vs Bacterial Pneumonia
- Input 1: Original X-ray (224x224x1)
- Input 2: Segmented lung (224x224x1)
- Output: Binary probability

## Important Notes

⚠️ **DO NOT** rename these files - the system expects exact filenames
⚠️ **DO NOT** modify model architectures
⚠️ Models are loaded once at startup for optimal performance
⚠️ Ensure all model files are present before starting the backend

## Model Loading

Models are automatically loaded at application startup in `main.py`:
1. Segmentation model reconstructed from config + weights
2. Stage-1 classifier loaded directly (.keras file)
3. Stage-2 classifier loaded directly (.keras file)

If any model fails to load, the application will not start.
