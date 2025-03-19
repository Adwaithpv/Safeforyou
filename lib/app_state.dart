import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class FFAppState extends ChangeNotifier {
  static FFAppState _instance = FFAppState._internal();

  factory FFAppState() {
    return _instance;
  }

  FFAppState._internal();

  static void reset() {
    _instance = FFAppState._internal();
  }

  Future initializePersistedState() async {
    prefs = await SharedPreferences.getInstance();
    _safeInit(() {
      _Number = prefs.getInt('ff_Number') ?? _Number;
    });
    _safeInit(() {
      _EmergencyContactsName =
          prefs.getString('ff_EmergencyContactsName') ?? _EmergencyContactsName;
    });
  }

  void update(VoidCallback callback) {
    callback();
    notifyListeners();
  }

  late SharedPreferences prefs;

  int _Number = 0;
  int get Number => _Number;
  set Number(int value) {
    _Number = value;
    prefs.setInt('ff_Number', value);
  }

  String _EmergencyContactsName = '';
  String get EmergencyContactsName => _EmergencyContactsName;
  set EmergencyContactsName(String value) {
    _EmergencyContactsName = value;
    prefs.setString('ff_EmergencyContactsName', value);
  }

  String _audioRecording = '';
  String get audioRecording => _audioRecording;
  set audioRecording(String value) {
    _audioRecording = value;
  }
}

void _safeInit(Function() initializeField) {
  try {
    initializeField();
  } catch (_) {}
}

Future _safeInitAsync(Function() initializeField) async {
  try {
    await initializeField();
  } catch (_) {}
}
