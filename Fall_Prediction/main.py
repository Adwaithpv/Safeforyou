# ================================
# FALL DETECTION BACKEND (FastAPI)
# ================================

# ========== IMPORTS ==========
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

# ========== FASTAPI APP SETUP ==========
app = FastAPI()

# ========== LOGGER CONFIGURATION ==========
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== CORS ENABLED FOR ALL ORIGINS ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== CONFIGURATION ==========
MODEL_JSON_PATH = r"path-to\fall_detection_model.json"            # Path to XGBoost model
SCALER_PATH = r"path-to\fall_detection_model_scaler.pkl"         # Path to sklearn scaler
WINDOW_SIZE = 75                                                 # Number of samples in a sliding window (e.g., 1.5s at 50Hz)
MIN_MOTION_THRESHOLD = 0.3                                       # Minimum motion threshold for activity detection
STATIONARY_ACC_STD = 0.05                                        # Standard deviation threshold to consider device as stationary
CONFIDENCE_BUFFER_SIZE = 10                                      # Buffer size for smoothing model predictions
OPTIMAL_THRESHOLD = 0.8                                          # Minimum confidence required to declare a fall

# ========== GLOBAL STATE ==========
sensor_buffer = deque(maxlen=WINDOW_SIZE)                        # Sensor data sliding window
confidence_buffer = deque(maxlen=CONFIDENCE_BUFFER_SIZE)         # Buffer to smooth predictions
calibration_baseline = None                                      # Optional calibration baseline
feature_names = None                                             # Expected feature order for model
model = None                                                     # Loaded XGBoost model
scaler = None                                                    # Preprocessing scaler

# ========== MODEL LOADING FUNCTION ==========
def load_model_components():
    """Load XGBoost model and preprocessing scaler"""
    global model, scaler, feature_names, OPTIMAL_THRESHOLD
    try:
        model = xgb.Booster()
        model.load_model(MODEL_JSON_PATH)
        logger.info("Model loaded successfully")

        scaler = joblib.load(SCALER_PATH)
        feature_names = scaler.feature_names_in_
        logger.info(f"Scaler loaded with {len(feature_names)} features")
        return True
    except Exception as e:
        logger.error(f"Model loading failed: {str(e)}")
        return False

# ========== CALIBRATION FUNCTION ==========
async def calibrate_sensors(calibration_samples: int = 50):
    """Calculate calibration baseline from the most recent sensor data"""
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

# ========== SAFE ARCCOS ==========
def safe_arccos(value):
    """Avoid math domain errors in arccos"""
    return np.arccos(np.clip(value, -1.0, 1.0))

# ========== FEATURE EXTRACTION FUNCTION ==========
def extract_window_features(window):
    """Generate a feature vector from a window of sensor values"""
    features = {}
    acc_cols = window[:, :3]
    gyro_cols = window[:, 3:]

    # Magnitude calculations
    acc_mag = np.linalg.norm(acc_cols, axis=1)
    gyro_mag = np.linalg.norm(gyro_cols, axis=1)

    # Basic motion metrics
    avg_gyro_movement = np.mean(np.abs(gyro_cols))
    max_acc_change = np.max(np.abs(np.diff(acc_cols, axis=0)))
    is_stationary = float(avg_gyro_movement < 0.1 and max_acc_change < 0.2)

    # Accelerometer features
    for j, axis in enumerate(['x', 'y', 'z']):
        axis_data = acc_cols[:, j]
        features.update({
            f'acc_{axis}_mean': float(np.mean(axis_data)),
            f'acc_{axis}_std': float(np.std(axis_data)),
            f'acc_{axis}_max': float(np.max(axis_data)),
            f'acc_{axis}_min': float(np.min(axis_data)),
            f'acc_{axis}_range': float(np.ptp(axis_data)),
        })

    # Gyroscope features
    for j, axis in enumerate(['x', 'y', 'z']):
        axis_data = gyro_cols[:, j]
        features.update({
            f'gyro_{axis}_mean': float(np.mean(axis_data)),
            f'gyro_{axis}_std': float(np.std(axis_data)),
            f'gyro_{axis}_max': float(np.max(axis_data)),
            f'gyro_{axis}_min': float(np.min(axis_data)),
            f'gyro_{axis}_range': float(np.ptp(axis_data)),
        })

    # Impact-related features
    features.update({
        'impact_peak': float(np.max(acc_mag) - np.mean(acc_mag)),
        'impact_duration': int(np.sum(acc_mag > np.mean(acc_mag) + 2*np.std(acc_mag))),
        'avg_gyro_movement': float(avg_gyro_movement),
        'max_acc_change': float(max_acc_change),
        'is_stationary': is_stationary
    })

    # Orientation change
    if len(window) >= 2:
        initial_acc = acc_cols[0]
        final_acc = acc_cols[-1]
        dot_product = np.dot(initial_acc, final_acc)
        norm_product = np.linalg.norm(initial_acc) * np.linalg.norm(final_acc)
        features['orientation_change'] = float(safe_arccos(dot_product / norm_product)) if norm_product > 0 else 0.0
    else:
        features['orientation_change'] = 0.0

    # Post-impact variation
    last_quarter = len(window) // 4
    features['post_impact_var'] = float(np.std(acc_mag[-last_quarter:])) if last_quarter > 0 else 0.0

    # Frequency-domain: Entropy
    features['acc_mag_entropy'] = float(entropy(np.histogram(acc_mag, bins=10)[0])) if len(acc_mag) >= 10 else 0.0

    return features

# ========== PREDICTION ENDPOINT ==========
@app.post("/upload_data/")
async def predict_fall(request: Request):
    """Receives a sensor sample, updates buffer, and predicts fall if enough data is collected"""
    global sensor_buffer, confidence_buffer

    try:
        data = await request.json()
        sensor_values = data.get("sensor_values")

        # Validate input
        if not sensor_values or len(sensor_values) != 6:
            raise HTTPException(status_code=400, detail="Invalid sensor data format")

        # Append to buffer
        sensor_buffer.append(sensor_values)

        # Not enough data yet
        if len(sensor_buffer) < WINDOW_SIZE:
            return {
                "status": "collecting",
                "samples": len(sensor_buffer),
                "required": WINDOW_SIZE
            }

        # Convert to numpy array
        window = np.array(list(sensor_buffer)[-WINDOW_SIZE:])

        # Ignore if stationary
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

        # Build dataframe
        features_df = pd.DataFrame([features], columns=feature_names)

        # Scale features
        features_scaled = scaler.transform(features_df)

        # Predict probability
        proba = model.predict(xgb.DMatrix(features_scaled))[0]
        confidence_buffer.append(proba)

        # Smooth prediction
        smoothed_proba = np.mean(confidence_buffer) if confidence_buffer else proba
        is_fall = smoothed_proba > OPTIMAL_THRESHOLD and features['is_stationary'] < 0.5

        # Log
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

# ========== CALIBRATION ENDPOINT ==========
@app.post("/calibrate/")
async def start_calibration():
    """Calibrates the system based on recent sensor data"""
    await calibrate_sensors()
    return {"status": "calibration_complete"}

# ========== STATUS CHECK ENDPOINT ==========
@app.get("/status/")
async def get_status():
    """Returns server and model status"""
    return {
        "buffer_size": len(sensor_buffer),
        "calibrated": calibration_baseline is not None,
        "threshold": OPTIMAL_THRESHOLD
    }

# ========== INITIALIZE MODEL ON STARTUP ==========
if not load_model_components():
    logger.error("Failed to initialize model components")

# ========== LOCAL DEVELOPMENT SERVER ==========
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
