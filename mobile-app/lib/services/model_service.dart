import 'package:tflite_flutter/tflite_flutter.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'dart:convert';
import 'dart:typed_data';
import 'package:image/image.dart' as img;

// Model Service - Handles both online and offline predictions
class ModelService {
  static final ModelService instance = ModelService._init();
  Interpreter? _interpreter;
  List<String>? _labels;
  final String apiUrl = 'https://your-api.com';

  ModelService._init();

  Future<void> loadModel() async {
    try {
      _interpreter = await Interpreter.fromAsset('plant_disease_model.tflite');
      _labels = await _loadLabels();
      print('Model loaded successfully');
    } catch (e) {
      print('Error loading model: $e');
    }
  }

  Future<List<String>> _loadLabels() async {
    // Load class names
    return [
      'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust',
      'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew',
      'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
      'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight',
      'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)',
      'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
      'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
      'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
      'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
      'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
      'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
      'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
      'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
      'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
      'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
    ];
  }

  List<String>? get labels => _labels;

  Future<Map<String, dynamic>> predictOffline(File imageFile) async {
    if (_interpreter == null) await loadModel();

    // Preprocess image
    img.Image? image = img.decodeImage(imageFile.readAsBytesSync());
    img.Image resized = img.copyResize(image!, width: 128, height: 128);

    // Convert to input tensor
    var input = _imageToByteListFloat32(resized);

    // Allocate output tensor
    var output = List.filled(1 * 38, 0.0).reshape([1, 38]);

    // Run inference
    _interpreter!.run(input, output);

    // Get prediction
    List<double> probabilities = output[0].cast<double>();
    int predictedIdx = probabilities.indexOf(probabilities.reduce((a, b) => a > b ? a : b));
    double confidence = probabilities[predictedIdx];

    return {
      'predicted_class': _labels![predictedIdx],
      'confidence': confidence,
      'probabilities': Map.fromIterables(_labels!, probabilities),
      'mode': 'offline'
    };
  }

  Uint8List _imageToByteListFloat32(img.Image image) {
    var convertedBytes = Float32List(1 * 128 * 128 * 3);
    var buffer = Float32List.view(convertedBytes.buffer);
    int pixelIndex = 0;

    for (int i = 0; i < 128; i++) {
      for (int j = 0; j < 128; j++) {
        var pixel = image.getPixel(j, i);
        buffer[pixelIndex++] = img.getRed(pixel) / 255.0;
        buffer[pixelIndex++] = img.getGreen(pixel) / 255.0;
        buffer[pixelIndex++] = img.getBlue(pixel) / 255.0;
      }
    }
    return convertedBytes.buffer.asUint8List();
  }

  Future<Map<String, dynamic>> predictOnline(
      File imageFile, Map<String, dynamic> metadata, String token) async {
    var request = http.MultipartRequest('POST', Uri.parse('$apiUrl/predict'));
    request.headers['Authorization'] = 'Bearer $token';
    request.files.add(await http.MultipartFile.fromPath('file', imageFile.path));
    request.fields['metadata'] = jsonEncode(metadata);
    request.fields['include_treatment'] = 'true';

    var response = await request.send();
    if (response.statusCode == 200) {
      var responseData = await response.stream.bytesToString();
      return jsonDecode(responseData);
    } else {
      throw Exception('Failed to get prediction from server');
    }
  }
}
