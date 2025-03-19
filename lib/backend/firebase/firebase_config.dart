import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

Future initFirebase() async {
  if (kIsWeb) {
    await Firebase.initializeApp(
        options: FirebaseOptions(
            apiKey: "AIzaSyB9UmR1wNRq_i8xs_8YcmbRWKeHG2OVvSc",
            authDomain: "social-hobby-activity-t-dv1typ.firebaseapp.com",
            projectId: "social-hobby-activity-t-dv1typ",
            storageBucket: "social-hobby-activity-t-dv1typ.firebasestorage.app",
            messagingSenderId: "615108194395",
            appId: "1:615108194395:web:dcaf4a5ed9e158f921cf7e"));
  } else {
    await Firebase.initializeApp();
  }
}
