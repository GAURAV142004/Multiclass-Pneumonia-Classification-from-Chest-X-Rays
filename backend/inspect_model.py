"""
Diagnostic script to inspect Stage-2 model architecture and test predictions.
Run from backend directory: python inspect_model.py
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras

MODEL_PATH = "app/models/dual_input_stage2_final.keras"

print("Loading model...")
model = keras.models.load_model(MODEL_PATH, compile=False)

print("\n=== MODEL INPUTS ===")
for i, inp in enumerate(model.inputs):
    print(f"  Input {i}: name={inp.name}, shape={inp.shape}, dtype={inp.dtype}")

print("\n=== MODEL OUTPUTS ===")
for i, out in enumerate(model.outputs):
    print(f"  Output {i}: name={out.name}, shape={out.shape}")

print("\n=== LAYERS (first 20) ===")
for layer in model.layers[:20]:
    try:
        in_shape  = layer.input_shape
        out_shape = layer.output_shape
    except Exception:
        in_shape  = "N/A"
        out_shape = "N/A"
    print(f"  [{layer.__class__.__name__}] {layer.name}")
    print(f"      in={in_shape}  out={out_shape}")

print("\n=== LAYERS (last 10) ===")
for layer in model.layers[-10:]:
    try:
        out_shape = layer.output_shape
    except Exception:
        out_shape = "N/A"
    print(f"  [{layer.__class__.__name__}] {layer.name}  out={out_shape}")

# ---------------------------------------------------------------
# Test inference with all four input combinations to expose bias
# ---------------------------------------------------------------
input_shape = tuple(model.inputs[0].shape[1:])   # e.g. (224, 224, 1) or (224, 224, 3)
print(f"\n=== INFERENCE TESTS (input shape per image: {input_shape}) ===")

def make_batch(pixel_value):
    arr = np.full((1,) + input_shape, pixel_value, dtype=np.float32)
    return arr

cases = [
    ("zeros [0]",         make_batch(0.0),   make_batch(0.0)),
    ("mid   [0.5]",       make_batch(0.5),   make_batch(0.5)),
    ("ones  [1.0]",       make_batch(1.0),   make_batch(1.0)),
    ("mid   [128/255]",   make_batch(0.502), make_batch(0.502)),
    ("255 range",         make_batch(128.0), make_batch(128.0)),
    ("255 full",          make_batch(255.0), make_batch(255.0)),
]

for label, orig, seg in cases:
    pred = model.predict([orig, seg], verbose=0)
    print(f"  Input={label:20s}  raw_output={pred}  shape={pred.shape}")

print("\nDone.")
