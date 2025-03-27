import numpy as np
import xgboost as xgb
import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()

# ✅ Load the trained XGBoost model
model_path = r"C:\Users\Skandesh Maadhav\Desktop\new\fall_detection_model.json"

try:
    model = xgb.XGBClassifier()
    model.load_model(model_path)
except Exception as e:
    raise RuntimeError(f"❌ Error loading model: {e}")

# ✅ Buffer to store sensor data for a window-based approach
window_size = 15
sensor_buffer = []
fall_detected = False  # 🚨 Flag to stop predictions after fall

@app.post("/upload_data/")
async def receive_sensor_data(data: dict):
    global sensor_buffer, fall_detected

    # 🚨 Stop making predictions after a fall
    if fall_detected:
        return {"message": "⚠️ Fall already detected. No further predictions until reset."}

    sensor_values = data.get("sensor_values", [])

    # ✅ Validate input format
    if not sensor_values or len(sensor_values) != 6:
        raise HTTPException(status_code=400, detail="❌ Expected 6 sensor values (accX, accY, accZ, gyroX, gyroY, gyroZ)")

    # ✅ Update buffer
    if len(sensor_buffer) >= window_size:
        sensor_buffer.pop(0)
    sensor_buffer.append(sensor_values)

    # ✅ Wait until buffer is full
    if len(sensor_buffer) < window_size:
        return {"message": "⏳ Collecting data, not enough for prediction yet"}

    # ✅ Convert buffer to NumPy array
    sensor_data_np = np.array(sensor_buffer)

    # ✅ Prepare input for model (Flatten the latest window)
    model_input = sensor_data_np[-1, :].reshape(1, -1)  # Latest sensor values

    # ✅ Predict using XGBoost model
    probability = model.predict_proba(model_input)[:, 1][0]  # Probability of fall
    prediction = probability > 0.91  # 🚨 Lowered threshold to 0.85 for sensitivity

    print(f"\n📊 Probability: {probability:.4f}, 🚨 Fall Detected: {prediction}")

    if prediction:  
        fall_detected = True  # 🚨 Stop future predictions

    return {
        "fall_detected": bool(prediction),
        "probability": float(probability)
    }

@app.post("/reset/")
async def reset_fall_detection():
    """Manually resets fall detection to allow new predictions."""
    global fall_detected
    fall_detected = False
    return {"message": "✅ Fall detection reset. Resuming predictions."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
