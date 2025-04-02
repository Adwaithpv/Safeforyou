import numpy as np
import xgboost as xgb
import joblib
import pandas as pd
from scipy.stats import entropy
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from collections import deque
import traceback
import logging
from typing import Optional

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Give proper path for model and scaler

# ==================== CONFIGURATION ====================
MODEL_JSON_PATH = r"path-to\fall_detection_model.json"
SCALER_PATH = r"path-to\fall_detection_model_scaler.pkl"
WINDOW_SIZE = 75  # 1.5 seconds at 50Hz
MIN_MOTION_THRESHOLD = 0.3  # Increased sensitivity threshold
STATIONARY_ACC_STD = 0.05   # Max std dev for stationary state
CONFIDENCE_BUFFER_SIZE = 10  # For smoothing predictions

# ==================== GLOBAL VARIABLES ====================
sensor_buffer = deque(maxlen=WINDOW_SIZE)
feature_names = None
model = None
scaler = None
OPTIMAL_THRESHOLD = 0.8  # More conservative default
confidence_buffer = deque(maxlen=CONFIDENCE_BUFFER_SIZE)
calibration_baseline = None

# ==================== MODEL LOADING ====================
def load_model_components():
    global model, scaler, feature_names, OPTIMAL_THRESHOLD
    
    try:
        # Load XGBoost model
        model = xgb.Booster()
        model.load_model(MODEL_JSON_PATH)
        logger.info("Model loaded successfully")
        
        # Load scaler
        scaler = joblib.load(SCALER_PATH)
        feature_names = scaler.feature_names_in_
        logger.info(f"Scaler loaded with {len(feature_names)} features")
    except Exception as e:
        logger.error(f"Model loading failed: {str(e)}")
        return False

# ==================== SENSOR CALIBRATION ====================
async def calibrate_sensors(calibration_samples: int = 50):
    """Establish baseline sensor readings"""
    global calibration_baseline
    logger.info("Starting sensor calibration...")
    
    temp_buffer = []
    for _ in range(calibration_samples):
        if sensor_buffer:
            temp_buffer.append(sensor_buffer[-1])
    
    if temp_buffer:
        calibration_baseline = np.mean(temp_buffer, axis=0)
        logger.info(f"Calibration complete. Baseline: {calibration_baseline}")
    else:
        logger.warning("Insufficient data for calibration")

# ==================== ENHANCED FEATURE EXTRACTION ====================
def safe_arccos(value):
    return np.arccos(np.clip(value, -1.0, 1.0))

def extract_window_features(window):
    """Enhanced feature extraction with false-positive reduction"""
    features = {}
    acc_cols = window[:, :3]
    gyro_cols = window[:, 3:]
    
    # Calculate magnitudes
    acc_mag = np.sqrt(np.sum(acc_cols**2, axis=1))
    gyro_mag = np.sqrt(np.sum(gyro_cols**2, axis=1))
    
    # Motion metrics - NEW
    avg_gyro_movement = np.mean(np.abs(gyro_cols))
    max_acc_change = np.max(np.abs(np.diff(acc_cols, axis=0)))
    is_stationary = float(avg_gyro_movement < 0.1 and max_acc_change < 0.2)
    
    # Time-domain features
    for j, axis in enumerate(['x', 'y', 'z']):
        axis_data = acc_cols[:, j]
        features.update({
            f'acc_{axis}_mean': float(np.mean(axis_data)),
            f'acc_{axis}_std': float(np.std(axis_data)),
            f'acc_{axis}_max': float(np.max(axis_data)),
            f'acc_{axis}_min': float(np.min(axis_data)),
            f'acc_{axis}_range': float(np.ptp(axis_data)),
        })
        
    for j, axis in enumerate(['x', 'y', 'z']):
        axis_data = gyro_cols[:, j]
        features.update({
            f'gyro_{axis}_mean': float(np.mean(axis_data)),
            f'gyro_{axis}_std': float(np.std(axis_data)),
            f'gyro_{axis}_max': float(np.max(axis_data)),
            f'gyro_{axis}_min': float(np.min(axis_data)),
            f'gyro_{axis}_range': float(np.ptp(axis_data)),
        })
    
    # Impact features
    features.update({
        'impact_peak': float(np.max(acc_mag) - np.mean(acc_mag)),
        'impact_duration': int(np.sum(acc_mag > np.mean(acc_mag) + 2*np.std(acc_mag))),
        'avg_gyro_movement': float(avg_gyro_movement),
        'max_acc_change': float(max_acc_change),
        'is_stationary': is_stationary
    })
    
    # Orientation features
    if len(window) >= 2:
        initial_acc = acc_cols[0]
        final_acc = acc_cols[-1]
        dot_product = np.dot(initial_acc, final_acc)
        norm_product = np.linalg.norm(initial_acc) * np.linalg.norm(final_acc)
        if norm_product > 0:
            features['orientation_change'] = float(safe_arccos(dot_product / norm_product))
    else:
        features['orientation_change'] = 0.0
    
    # Post-impact features
    last_quarter = len(window) // 4
    features['post_impact_var'] = float(np.std(acc_mag[-last_quarter:])) if last_quarter > 0 else 0.0
    
    # Frequency features
    features['acc_mag_entropy'] = float(entropy(np.histogram(acc_mag, bins=10)[0])) if len(acc_mag) >= 10 else 0.0
    
    return features

# ==================== API ENDPOINTS ====================
@app.post("/upload_data/")
async def predict_fall(request: Request):
    global sensor_buffer, confidence_buffer
    
    try:
        data = await request.json()
        sensor_values = data.get("sensor_values")
        
        # Validate input
        if not sensor_values or len(sensor_values) != 6:
            raise HTTPException(status_code=400, detail="Invalid sensor data format")
        
        # Add to buffer
        sensor_buffer.append(sensor_values)
        
        # Wait until we have enough data
        if len(sensor_buffer) < WINDOW_SIZE:
            return {
                "status": "collecting",
                "samples": len(sensor_buffer),
                "required": WINDOW_SIZE
            }
        
        # Convert to numpy array
        window = np.array(list(sensor_buffer)[-WINDOW_SIZE:])
        
        # Check for stationary device
        acc_std = np.std(window[:, :3])
        if acc_std < STATIONARY_ACC_STD:
            return {
                "status": "stationary",
                "fall_detected": False,
                "confidence": 0.0,
                "metrics": {"acc_std": float(acc_std)}
            }
        
        # Extract features
        features = extract_window_features(window)
        
        # Apply calibration if available
        if calibration_baseline is not None:
            window_calibrated = window - calibration_baseline
            features.update(extract_window_features(window_calibrated))
        
        # Create feature dataframe
        features_df = pd.DataFrame([features], columns=feature_names)
        
        # Scale features
        features_scaled = scaler.transform(features_df)
        
        # Predict
        proba = model.predict(xgb.DMatrix(features_scaled))[0]
        confidence_buffer.append(proba)
        
        # Apply smoothing
        smoothed_proba = np.mean(confidence_buffer) if confidence_buffer else proba
        is_fall = smoothed_proba > OPTIMAL_THRESHOLD and features['is_stationary'] < 0.5
        
        # Log for debugging
        logger.info(f"Prediction: {proba:.4f} (Smoothed: {smoothed_proba:.4f}) | Fall: {is_fall} | Stationary: {features['is_stationary']}")
        
        return {
            "status": "processed",
            "fall_detected": bool(is_fall),
            "confidence": float(smoothed_proba),
            "threshold": float(OPTIMAL_THRESHOLD),
            "metrics": {
                "acc_std": float(acc_std),
                "is_stationary": features['is_stationary'],
                "orientation_change": features.get('orientation_change', 0)
            }
        }
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calibrate/")
async def start_calibration():
    await calibrate_sensors()
    return {"status": "calibration_complete"}

@app.get("/status/")
async def get_status():
    return {
        "buffer_size": len(sensor_buffer),
        "calibrated": calibration_baseline is not None,
        "threshold": OPTIMAL_THRESHOLD
    }

# Initialize
if not load_model_components():
    logger.error("Failed to initialize model components")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
