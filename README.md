# Safe For You

A Flutter application focused on safety and security features, built with modern Flutter practices and Firebase integration. The app includes an advanced ML model for detecting distress in speech patterns.

## Features

- Firebase Authentication with multiple sign-in methods
- Real-time location tracking
- Cloud Firestore integration for data storage
- Cross-platform support (iOS, Android, Web)
- Modern UI with Material Design
- Localization support
- Secure data handling
- File management and media handling
- **AI-Powered Distress Detection**
  - Speech pattern analysis for distress detection
  - Real-time audio processing
  - TensorFlow Lite integration for mobile deployment
  - High-accuracy deep learning model

## Getting Started

### Prerequisites

- Flutter SDK (>=3.0.0)
- Dart SDK (>=3.0.0)
- Firebase project setup
- Android Studio / VS Code with Flutter extensions
- Python 3.x (for ML model development)
- TensorFlow 2.x (for ML model development)

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

5. Set up the ML model:
   - Navigate to the Women Safety directory
   - Install Python dependencies:
   ```bash
   pip install tensorflow pandas numpy scikit-learn joblib
   ```
   - The pre-trained model files are included in the repository:
     - `speech_distress_model.tflite` (mobile-optimized)
     - `speech_distress_model.h5` (full model)
     - `scaler.save` (feature scaler)

6. Run the app:
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
└── Women Safety/          # ML Model components
    ├── model.py          # Model architecture and training
    ├── deploy.py         # Model deployment script
    ├── speech_distress_model.tflite  # Mobile-optimized model
    ├── speech_distress_model.h5      # Full model
    └── scaler.save       # Feature scaler
```

## ML Model Details

The app includes a sophisticated deep learning model for detecting distress in speech patterns:

- **Architecture**: Hybrid CNN-LSTM with attention mechanism
- **Features**: 
  - Audio signal processing
  - Mel-frequency cepstral coefficients (MFCC)
  - Spectral features
  - Temporal features
- **Optimization**:
  - Focal loss for handling class imbalance
  - Attention mechanism for better feature learning
  - TensorFlow Lite conversion for mobile deployment
- **Performance**:
  - Real-time processing
  - Mobile-optimized inference
  - Balanced accuracy across different speech patterns

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
