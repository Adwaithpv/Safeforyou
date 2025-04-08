import numpy as np
import librosa
import joblib
import tensorflow as tf
import speech_recognition as sr
import tempfile
import os

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="speech_distress_model.tflite")
interpreter.allocate_tensors()

# Retrieve input and output details for inference
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load the scaler for feature normalization
scaler = joblib.load("scaler.save")

# Read the expected feature column names
with open("feature_columns.txt", "r") as f:
    feature_columns = f.read().splitlines()

# Define distress-related keywords for transcription matching
keywords = ["help", "emergency", "save me", "please help", "danger", "call police", "stop"]
DISTRESS_THRESHOLD = 0.6  # Probability threshold to consider a distress detection

# ---------------------- Feature Extraction Function -------------------------

def extract_features(y, sr):
    """
    Extracts audio features used for distress prediction.
    Includes MFCC, ZCR, spectral centroid, RMS, and chroma features.

    Args:
        y (np.array): Audio time series.
        sr (int): Sampling rate.

    Returns:
        np.array: Feature vector.
    """
    features = []
    
    # MFCC (Mel-Frequency Cepstral Coefficients)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    features.extend(mfcc_mean)

    # Zero Crossing Rate
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    features.append(zcr)

    # Spectral Centroid
    spec_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    features.append(spec_centroid)

    # Root Mean Square Energy
    rms = np.mean(librosa.feature.rms(y=y))
    features.append(rms)

    # Chroma STFT
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma.T, axis=0)
    features.extend(chroma_mean)

    return np.array(features)

# ---------------------- Transcription Function ----------------------

def transcribe_audio(file_path):
    """
    Transcribes the given audio file using Google's speech recognition API.

    Args:
        file_path (str): Path to audio file.

    Returns:
        str: Transcribed lowercase text, or empty string if failed.
    """
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio).lower()
    except Exception:
        return ""

# ---------------------- Distress Prediction Function ----------------------

def predict_distress(file_path):
    """
    Predicts distress probability from the given audio file.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        float or None: Distress probability (0 to 1), or None if failed.
        np.array or None: Feature vector used, or None if extraction failed.
    """
    try:
        y, sr_audio = librosa.load(file_path, sr=None)
        features = extract_features(y, sr_audio)
    except Exception as e:
        print(f"Feature extraction failed: {e}")
        return None, None

    # Ensure feature vector matches expected length
    if len(features) < len(feature_columns):
        features = np.pad(features, (0, len(feature_columns) - len(features)))
    else:
        features = features[:len(feature_columns)]

    try:
        scaled_features = scaler.transform([features])
        reshaped_input = scaled_features.reshape((1, len(feature_columns), 1)).astype(np.float32)

        # Run inference using TFLite model
        interpreter.set_tensor(input_details[0]['index'], reshaped_input)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])[0][0]
        return prediction, features
    except Exception as e:
        print(f"Prediction failed: {e}")
        return None, None

# ---------------------- Live Recording + Detection Function ----------------------

def detect_distress_once(duration=5):
    """
    Records audio for a fixed duration, transcribes it, runs prediction,
    and prints the detection result based on distress threshold and keywords.

    Args:
        duration (int): Duration to record in seconds.
    """
    recognizer = sr.Recognizer()
    print(f"\nRecording {duration} seconds of audio for distress detection...\n")
    
    # Record from microphone
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, phrase_time_limit=duration)

    # Save temporary audio file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio.get_wav_data())
        temp_path = f.name

    # Transcribe and predict
    transcript = transcribe_audio(temp_path)
    prediction, _ = predict_distress(temp_path)
    keyword_hit = any(word in transcript for word in keywords)

    # Print results
    print(f"\nTranscribed Text: {transcript if transcript else '[Unable to transcribe]'}")
    if prediction is not None:
        if prediction > DISTRESS_THRESHOLD and keyword_hit:
            print("HIGH ALERT: Distress detected via voice + keywords.")
        elif prediction > DISTRESS_THRESHOLD:
            print("Voice distress detected.")
        elif keyword_hit:
            print("Keyword-based distress detected.")
        else:
            print("No distress detected.")

    # Clean up temporary audio file
    os.remove(temp_path)

# ---------------------- Entry Point ----------------------

if __name__ == "__main__":
    detect_distress_once()
