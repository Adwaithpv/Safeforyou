# Women Safety - Voice Distress Detection System

A machine learning-based system that detects distress signals from voice recordings using both acoustic features and keyword analysis. The system is designed to help identify potential emergency situations through voice analysis.

## Project Overview

This project implements a deep learning model that analyzes voice recordings to detect distress signals. It combines:
- Acoustic feature analysis using a deep neural network
- Keyword-based detection
- Real-time audio processing capabilities

## Features

- Real-time audio recording and analysis
- Distress detection through voice patterns
- Keyword-based emergency detection
- Web interface for easy interaction
- Support for both file upload and direct recording
- Mobile-friendly interface

## Technical Architecture

The system consists of several key components:

1. **Deep Learning Model**
   - Convolutional Neural Network (CNN) for feature extraction
   - Bidirectional LSTM for temporal pattern recognition
   - Attention mechanism for improved detection
   - Focal loss for handling class imbalance

2. **Audio Processing**
   - Feature extraction from audio files
   - Real-time audio recording
   - Speech-to-text transcription

3. **Web Interface**
   - Gradio-based web application
   - Support for file upload and direct recording
   - Real-time feedback

## Project Structure

```
├── app.py                 # Main web application
├── model.py              # Deep learning model implementation
├── lite_deploy.py        # Lightweight deployment utilities
├── deploy.py             # Deployment utilities
├── Feature Extract.py    # Feature extraction utilities
├── labels.csv            # Dataset labels
├── features.csv          # Extracted features
├── feature_columns.txt   # Feature column names
├── speech_distress_model.h5    # Trained model
├── speech_distress_model.tflite # Lightweight model
├── scaler.save           # Feature scaler
├── class_weights.json    # Class weights for training
├── training_history.pkl  # Training history
├── logs/                 # Training logs
├── flagged/             # Directory for flagged recordings
└── CREMA-D/             # Dataset directory
```

## Setup and Installation

1. Clone the repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Launch the web application
2. Choose between:
   - Uploading an audio file
   - Recording directly through the microphone
3. The system will analyze the audio and provide:
   - Distress detection result
   - Audio transcript
   - Confidence level

## Model Details

The model architecture includes:
- Multiple Conv1D layers for feature extraction
- Bidirectional LSTM layers for temporal analysis
- Attention mechanism for improved detection
- Dense layers for final classification

Training metrics:
- Focal loss for handling class imbalance
- Early stopping to prevent overfitting
- Learning rate reduction on plateau
- Model checkpointing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- CREMA-D dataset for training data
- TensorFlow and Keras for deep learning framework
- Gradio for web interface 