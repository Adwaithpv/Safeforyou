// Import necessary packages
import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:sensors_plus/sensors_plus.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(FallDetectionApp());
}

// Main StatefulWidget for the fall detection system
class FallDetectionApp extends StatefulWidget {
  @override
  _FallDetectionAppState createState() => _FallDetectionAppState();
}

class _FallDetectionAppState extends State<FallDetectionApp> {
  // Status message displayed to the user
  String fallStatus = "Monitoring...";

  // Flags to manage fall detection and connectivity state
  bool fallDetected = false;
  bool connectionLost = false;

  // Variables to store the latest sensor readings
  double accX = 0, accY = 0, accZ = 0;
  double gyroX = 0, gyroY = 0, gyroZ = 0;

  @override
  void initState() {
    super.initState();
    startListening();
  }

  // Start listening to accelerometer and gyroscope data
  void startListening() {
    accelerometerEvents.listen((event) {
      if (!fallDetected) {
        setState(() {
          accX = event.x;
          accY = event.y;
          accZ = event.z;
        });
        sendDataToServer();
      }
    });

    gyroscopeEvents.listen((event) {
      if (!fallDetected) {
        setState(() {
          gyroX = event.x;
          gyroY = event.y;
          gyroZ = event.z;
        });
        sendDataToServer();
      }
    });
  }

  // Sends sensor data to the backend API for fall prediction
  Future<void> sendDataToServer() async {
    if (fallDetected) return;

    final url = Uri.parse("http://your-ip-address/upload_data/");
    final body = jsonEncode({
      "sensor_values": [accX, accY, accZ, gyroX, gyroY, gyroZ]
    });

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: body,
      );

      if (response.statusCode == 200) {
        final result = jsonDecode(response.body);
        print("Server Response: $result");

        if (result.containsKey("fall_detected")) {
          bool detected = result["fall_detected"];

          setState(() {
            fallDetected = detected;
            fallStatus = detected ? "Fall Detected!" : "No Fall";
          });
        } else if (result.containsKey("message")) {
          setState(() {
            fallStatus = "Fall Detected!";
            fallDetected = true;
          });
        }
      } else {
        throw Exception("Server error: ${response.body}");
      }
    } catch (e) {
      print("Failed to send data: $e");

      setState(() {
        fallStatus = "Connection Lost";
        connectionLost = true;
      });
    }
  }

  // Resets the UI and monitoring flags after a fall is detected
  void resetMonitoring() {
    setState(() {
      fallDetected = false;
      fallStatus = "Monitoring...";
      connectionLost = false;
    });
  }

  // Build the user interface
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text("Fall Detection System")),
        body: Padding(
          padding: EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text("Accelerometer", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              Text("X: $accX, Y: $accY, Z: $accZ"),
              SizedBox(height: 20),
              Text("Gyroscope", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              Text("X: $gyroX, Y: $gyroY, Z: $gyroZ"),
              SizedBox(height: 40),
              Text(
                fallStatus,
                style: TextStyle(
                  fontSize: 24,
                  color: fallDetected
                      ? Colors.red
                      : (connectionLost ? Colors.orange : Colors.green),
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(height: 20),
              if (fallDetected)
                ElevatedButton(
                  onPressed: resetMonitoring,
                  child: Text("Reset Monitoring"),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
