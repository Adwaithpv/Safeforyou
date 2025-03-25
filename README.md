# Safe For You

A Flutter application focused on safety and security features, built with modern Flutter practices and Firebase integration.

## Features

- Firebase Authentication with multiple sign-in methods
- Real-time location tracking
- Cloud Firestore integration for data storage
- Cross-platform support (iOS, Android, Web)
- Modern UI with Material Design
- Localization support
- Secure data handling
- File management and media handling

## Getting Started

### Prerequisites

- Flutter SDK (>=3.0.0)
- Dart SDK (>=3.0.0)
- Firebase project setup
- Android Studio / VS Code with Flutter extensions

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

5. Run the app:
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
└── firebase/              # Firebase configuration
```

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
- All contributors who have helped with this project
