import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

Future initFirebase() async {
  if (kIsWeb) {
    await Firebase.initializeApp(
        options: FirebaseOptions(
            apiKey: "AIzaSyBCYYxwS4ygH_92zJccB97tEPziSkU2kcs",
            authDomain: "safeforyou-99d78.firebaseapp.com",
            projectId: "safeforyou-99d78",
            storageBucket: "safeforyou-99d78.firebasestorage.app",
            messagingSenderId: "99173960298",
            appId: "1:99173960298:web:bf6db8d77ea8b504331813",
            measurementId: "G-RMC5ZJ3YQX"));
  } else {
    await Firebase.initializeApp();
  }
}
