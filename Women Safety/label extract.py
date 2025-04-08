import os
import pandas as pd

# Path to the CREMA-D dataset directory
DATASET_PATH = "CREMA-D/"

# Mapping of emotion codes to their corresponding emotion names
EMOTIONS = {
    "ANG": "angry",
    "DIS": "disgust",
    "FEA": "fear",
    "HAP": "happy",
    "NEU": "neutral",
    "SAD": "sad"
}

# Emotions considered as indicators of distress
DISTRESS_LABELS = {"angry", "disgust", "fear"}

# List to hold tuples of (filename, emotion, distress label)
data = []

# Loop through all .wav files in the dataset directory
for file in os.listdir(DATASET_PATH):
    if file.endswith(".wav"):
        parts = file.split("_")  # e.g., "1001_TIE_FEA_XX.wav" → ['1001', 'TIE', 'FEA', 'XX.wav']
        emotion_code = parts[2]  # Extract the third part (emotion code)
        if emotion_code in EMOTIONS:
            emotion = EMOTIONS[emotion_code]
            label = 1 if emotion in DISTRESS_LABELS else 0  # 1 for distress, 0 for non-distress
            data.append((file, emotion, label))

# Create a DataFrame with the extracted labels
df = pd.DataFrame(data, columns=["filename", "emotion", "distress?"])

# Save the DataFrame as a CSV file for future use
df.to_csv("labels.csv", index=False)
