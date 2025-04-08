import numpy as np
import librosa
import joblib
import tensorflow as tf
import speech_recognition as sr
import tempfile
import os

# Load the pre-trained deep learning model and the feature scaler
model = tf.keras.models.load_model("test_speech_distress_model.h5", compile=False)
scaler = joblib.load("scaler.save")

# Load feature column names to maintain feature shape consistency
with open("feature_columns.txt", "r") as f:
    feature_columns = f.read().splitlines()

# Keywords to look for in transcriptions
keywords = ["help", "emergency", "save me", "please help", "danger", "call police"]
DISTRESS_THRESHOLD = 0.6  # Threshold above which prediction is considered distress

def extract_features(y, sr):
    """
    Extracts audio features from a given waveform and sample rate.
    
    Features include:
        - MFCC (20 coefficients)
        - Zero Crossing Rate
        - Spectral Centroid
        - Root Mean Square Energy (RMS)
        - Chroma Frequencies

    Args:
        y (np.ndarray): Audio time series
        sr (int): Sampling rate

    Returns:
        np.ndarray: Flattened feature vector
    """
    features = []

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    features.extend(mfcc_mean)

    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    features.append(zcr)

    spec_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    features.append(spec_centroid)

    rms = np.mean(librosa.feature.rms(y=y))
    features.append(rms)

    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma.T, axis=0)
    features.extend(chroma_mean)

    return np.array(features)

def transcribe_audio(file_path):
    """
    Converts speech in an audio file to text using Google Speech Recognition.

    Args:
        file_path (str): Path to the audio file

    Returns:
        str: Lowercase transcription or empty string if failed
    """
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio).lower()
    except Exception:
        return ""

def predict_distress(file_path):
    """
    Predicts distress from a given audio file using a trained deep learning model.

    Args:
        file_path (str): Path to the audio file

    Returns:
        tuple: (prediction score [float], feature vector [np.ndarray])
    """
    try:
        y, sr_audio = librosa.load(file_path, sr=None)
        features = extract_features(y, sr_audio)
    except Exception as e:
        print(f"Feature extraction failed: {e}")
        return None, None

    # Ensure the feature vector has the same number of elements as expected
    if len(features) < len(feature_columns):
        features = np.pad(features, (0, len(feature_columns) - len(features)))
    else:
        features = features[:len(feature_columns)]

    try:
        scaled_features = scaler.transform([features])  # Scale features
        scaled_features = scaled_features.reshape((1, len(feature_columns), 1))  # Reshape for model
        prediction = model.predict(scaled_features)[0][0]
        return prediction, features
    except Exception as e:
        print(f"Prediction failed: {e}")
        return None, None

def detect_distress_once(duration=5):
    """
    Records audio from the microphone for a specified duration and performs:
    1. Voice-based distress prediction
    2. Keyword detection from transcription

    Args:
        duration (int): Length of audio to record in seconds
    """
    recognizer = sr.Recognizer()
    print(f"\nRecording {duration} seconds of audio for distress detection...\n")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, phrase_time_limit=duration)

    # Save recorded audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio.get_wav_data())
        temp_path = f.name

    transcript = transcribe_audio(temp_path)
    prediction, _ = predict_distress(temp_path)
    keyword_hit = any(word in transcript for word in keywords)

    print(f"\nTranscribed Text: {transcript if transcript else '[Unable to transcribe]'}")
    
    # Alert logic based on model prediction and transcription
    if prediction is not None:
        if prediction > DISTRESS_THRESHOLD and keyword_hit:
            print("HIGH ALERT: Distress detected via voice + keywords.")
        elif prediction > DISTRESS_THRESHOLD:
            print("Voice distress detected.")
        elif keyword_hit:
            print("Keyword-based distress detected.")
        else:
            print("No distress detected.")

    os.remove(temp_path)  # Clean up temporary audio file

# Run only if executed directly
if __name__ == "__main__":
    detect_distress_once()
