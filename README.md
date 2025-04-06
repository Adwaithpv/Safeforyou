# Safe For You

A Flutter application focused on safety and security features, built with modern Flutter practices and Firebase integration. The app includes advanced ML models for detecting distress in speech patterns, fall detection, and real-time location tracking with geo-fencing capabilities.

## Features

- Firebase Authentication with multiple sign-in methods
- Real-time location tracking with geo-fencing
- Cloud Firestore integration for data storage
- Cross-platform support (iOS, Android, Web)
- Modern UI with Material Design
- Localization support
- Secure data handling
- File management and media handling
- **AI-Powered Features**:
  - Speech pattern analysis for distress detection
  - Real-time audio processing
  - TensorFlow Lite integration for mobile deployment
  - High-accuracy deep learning model
  - Fall detection using accelerometer data
  - Geo-fencing for location-based safety alerts
  - Live location tracking and sharing

## Getting Started

### Prerequisites

- Flutter SDK (>=3.0.0)
- Dart SDK (>=3.0.0)
- Firebase project setup
- Android Studio / VS Code with Flutter extensions
- Python 3.x (for ML model development)
- TensorFlow 2.x (for ML model development)
- Node.js (for web components)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/safeforyou.git
```

2. Navigate to the project directory:
```bash
cd safeforyou
```

3. Install dependencies:
```bash
flutter pub get
```

4. Set up Firebase:
   - Create a new Firebase project
   - Add your Android and iOS apps to the Firebase project
   - Download and add the configuration files:
     - `google-services.json` for Android
     - `GoogleService-Info.plist` for iOS

5. Set up the ML models:
   - Navigate to the Women Safety directory for speech distress detection
   - Navigate to the Fall_Prediction directory for fall detection
   - Install Python dependencies:
   ```bash
   pip install tensorflow pandas numpy scikit-learn joblib
   ```
   - The pre-trained model files are included in their respective directories

6. Set up Geo-Fencing:
   - Navigate to the Geo-Fencing directory
   - Install required Python packages:
   ```bash
   pip install pandas beautifulsoup4
   ```
   - Run the web scraping and article extraction scripts

7. Set up Live Tracking:
   - Navigate to the Live Tracking directory
   - Install Node.js dependencies:
   ```bash
   npm install
   ```
   - Configure Firebase credentials

8. Run the app:
```bash
flutter run
```

## Project Structure

```
safeforyou/
├── lib/                    # Main source code
├── assets/                 # Project assets
│   ├── images/            # Image assets
│   ├── fonts/             # Custom fonts
│   ├── videos/            # Video assets
│   ├── audios/            # Audio assets
│   └── rive_animations/   # Rive animations
├── test/                   # Test files
├── web/                    # Web-specific files
├── android/               # Android-specific files
├── ios/                   # iOS-specific files
├── firebase/              # Firebase configuration
├── Women Safety/          # Speech Distress Detection
│   ├── model.py          # Model architecture and training
│   ├── deploy.py         # Model deployment script
│   ├── speech_distress_model.tflite  # Mobile-optimized model
│   ├── speech_distress_model.h5      # Full model
│   └── scaler.save       # Feature scaler
├── Fall_Prediction/       # Fall Detection System
│   ├── main.py           # Fall detection model
│   ├── main.dart         # Flutter integration
│   ├── fall_detection_model.pkl      # Trained model
│   └── fall_detection_model_scaler.pkl # Feature scaler
├── Geo-Fencing/          # Location-based Safety
│   ├── webscraping.py    # News data collection
│   ├── article_extraction.py # Article processing
│   ├── map.html          # Interactive map
│   └── *.csv             # Safety data
└── Live Tracking/        # Real-time Location
    ├── app.py           # Backend server
    ├── script.js        # Frontend logic
    ├── index.html       # Web interface
    └── twil.py          # Twilio integration
```

## ML Model Details

The app includes multiple sophisticated deep learning models:

1. **Speech Distress Detection**:
   - Architecture: Hybrid CNN-LSTM with attention mechanism
   - Features: Audio signal processing, MFCC, Spectral features
   - Optimization: Focal loss, Attention mechanism
   - Performance: Real-time processing, Mobile-optimized inference

2. **Fall Detection**:
   - Architecture: Machine Learning model for accelerometer data
   - Features: Motion patterns, Acceleration metrics
   - Optimization: Real-time processing, Low latency
   - Performance: High accuracy in fall detection

## Dependencies

Key dependencies include:
- `firebase_core`: Firebase core functionality
- `firebase_auth`: Authentication
- `cloud_firestore`: Database
- `firebase_storage`: File storage
- `go_router`: Navigation
- `provider`: State management
- `flutter_native_splash`: Splash screen
- `google_sign_in`: Google authentication
- `sign_in_with_apple`: Apple authentication
- TensorFlow Lite for Flutter
- Audio processing libraries
- Location services
- Accelerometer sensors
- Web scraping tools
- Twilio for notifications

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flutter team for the amazing framework
- Firebase team for the backend services
- TensorFlow team for the ML framework
- All contributors who have helped with this project
