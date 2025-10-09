// Flutter Mobile App for Plant Disease Detection
// Supports offline mode, caching, and TFLite integration

import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(PlantDiseaseApp());
}

class PlantDiseaseApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Plant Disease Detector',
      theme: ThemeData(
        primarySwatch: Colors.green,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: HomeScreen(),
    );
  }
}