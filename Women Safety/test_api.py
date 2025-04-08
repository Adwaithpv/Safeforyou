# Import necessary libraries
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import os
import numpy as np
import librosa
import joblib
import tensorflow as tf
import tempfile
import speech_recognition as sr

# Initialize the FastAPI app
app = FastAPI()

# Load the TFLite model and allocate tensors
interpreter = tf.lite.Interpreter(model_path="speech_distress_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load the StandardScaler used during training
scaler = joblib.load("scaler.save")

# Load the order of feature columns
with open("feature_columns.txt", "r") as f:
    feature_columns = f.read().splitlines()

# List of distress-related keywords for transcription analysis
keywords = ["help", "emergency", "save me", "please help", "danger", "call police", "stop"]

# Threshold to determine distress based on model prediction
DISTRESS_THRESHOLD = 0.6

# Feature extraction from raw audio signal
def extract_features(y, sr):
    features = []

    # Extract MFCCs (20 coefficients)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    features.extend(mfcc_mean)

    # Zero-crossing rate
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    features.append(zcr)

    # Spectral centroid
    spec_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    features.append(spec_centroid)

    # Root Mean Square Energy
    rms = np.mean(librosa.feature.rms(y))
    features.append(rms)

    # Chroma features (12 coefficients)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma.T, axis=0)
    features.extend(chroma_mean)

    return np.array(features)

# Transcribe audio using Google's speech recognition API
def transcribe_audio(file_path):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text.lower()
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""

# Perform inference using the TFLite model
def predict_distress(file_path):
    y, sr_audio = librosa.load(file_path, sr=None)
    features = extract_features(y, sr_audio)

    # Ensure consistency with training features
    if len(features) < len(feature_columns):
        features = np.pad(features, (0, len(feature_columns) - len(features)))
    else:
        features = features[:len(feature_columns)]

    # Preprocess and reshape features for TFLite model
    scaled = scaler.transform([features])
    reshaped_input = scaled.reshape((1, len(feature_columns), 1)).astype(np.float32)

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], reshaped_input)
    interpreter.invoke()
    prediction = interpreter.get_tensor(output_details[0]['index'])[0][0]

    return prediction

# Home route to render a basic HTML page for live recording and upload
@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
    <head><title>Live Audio Input</title></head>
    <body>
        <h1>🎙️ Live Distress Detection</h1>
        <button onclick="startRecording()">Start Recording</button>
        <button onclick="stopRecording()">Stop & Upload</button>
        <p id="status">Status: Idle</p>
        <p id="result"></p>
        <script>
        let mediaRecorder;
        let audioChunks = [];

        // Start audio recording
        function startRecording() {
            navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                document.getElementById('status').innerText = 'Status: Recording...';
                mediaRecorder.ondataavailable = e => {
                    audioChunks.push(e.data);
                };
            });
        }

        // Stop recording, upload the audio and fetch prediction result
        function stopRecording() {
            mediaRecorder.stop();
            mediaRecorder.onstop = () => {
                document.getElementById('status').innerText = 'Status: Uploading...';
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('file', audioBlob, 'recording.wav');

                fetch('/predict', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').innerText = JSON.stringify(data, null, 2);
                    document.getElementById('status').innerText = 'Status: Done ';
                });
            };
        }
        </script>
    </body>
    </html>
    """

# API route to handle uploaded audio file and return prediction results
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(await file.read())
        temp_path = temp.name

    # Speech-to-text transcription
    transcript = transcribe_audio(temp_path)

    # Keyword detection
    keyword_hit = any(word in transcript for word in keywords)

    # Voice-based distress prediction
    prediction_score = predict_distress(temp_path)

    # Clean up temp file
    os.remove(temp_path)

    # Combine prediction and keyword check to determine status
    return {
        "transcript": transcript,
        "keyword_detected": keyword_hit,
        "prediction_score": prediction_score,
        "status": (
            "High Alert: Voice + Keywords"
            if prediction_score > DISTRESS_THRESHOLD and keyword_hit
            else "Voice distress detected"
            if prediction_score > DISTRESS_THRESHOLD
            else "Keyword-based distress detected"
            if keyword_hit
            else "No distress detected"
        )
    }
