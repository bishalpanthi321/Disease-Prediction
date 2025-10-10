import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:geolocator/geolocator.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:io';
import 'dart:convert';
import '../services/database_helper.dart';
import '../services/model_service.dart';
import '../services/connectivity_service.dart';
import 'history_screen.dart';
import 'feedback_dialog.dart';

// Main Home Screen
class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  File? _image;
  Map<String, dynamic>? _prediction;
  bool _isLoading = false;
  bool _isOnline = true;
  final ImagePicker _picker = ImagePicker();
  Position? _currentPosition;

  @override
  void initState() {
    super.initState();
    _checkConnectivity();
    _getCurrentLocation();
    ModelService.instance.loadModel();
  }

  Future<void> _checkConnectivity() async {
    await ConnectivityService.instance.initialize();
    setState(() {
      _isOnline = ConnectivityService.instance.isOnline;
    });
  }

  Future<void> _getCurrentLocation() async {
    try {
      _currentPosition = await Geolocator.getCurrentPosition(
          desiredAccuracy: LocationAccuracy.high);
    } catch (e) {
      print('Error getting location: $e');
    }
  }

  Future<void> _takePicture() async {
    final XFile? photo = await _picker.pickImage(
        source: ImageSource.camera, imageQuality: 85);
    if (photo != null) {
      setState(() {
        _image = File(photo.path);
      });
      await _analyzePlant();
    }
  }

  Future<void> _pickImage() async {
    final XFile? image = await _picker.pickImage(
        source: ImageSource.gallery, imageQuality: 85);
    if (image != null) {
      setState(() {
        _image = File(image.path);
      });
      await _analyzePlant();
    }
  }

  Future<void> _analyzePlant() async {
    if (_image == null) return;

    setState(() {
      _isLoading = true;
    });

    try {
      Map<String, dynamic> metadata = {
        'timestamp': DateTime.now().toIso8601String(),
        'location': _currentPosition != null
            ? {
                'latitude': _currentPosition!.latitude,
                'longitude': _currentPosition!.longitude
              }
            : null,
      };

      Map<String, dynamic> result;

      if (_isOnline) {
        // Try online prediction first
        try {
          String token = await _getAuthToken();
          result = await ModelService.instance.predictOnline(
              _image!, metadata, token);
          result['mode'] = 'online';
        } catch (e) {
          print('Online prediction failed, falling back to offline: $e');
          result = await ModelService.instance.predictOffline(_image!);
        }
      } else {
        // Use offline model
        result = await ModelService.instance.predictOffline(_image!);
      }

      // Save to local database
      await DatabaseHelper.instance.insertPrediction({
        'id': DateTime.now().millisecondsSinceEpoch.toString(),
        'timestamp': DateTime.now().toIso8601String(),
        'predicted_class': result['predicted_class'],
        'confidence': result['confidence'],
        'image_path': _image!.path,
        'severity': result['severity'] ?? 'unknown',
        'synced': _isOnline ? 1 : 0,
        'metadata': jsonEncode(metadata)
      });

      setState(() {
        _prediction = result;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      _showError('Error analyzing image: $e');
    }
  }

  Future<String> _getAuthToken() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getString('auth_token') ?? '';
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), backgroundColor: Colors.red),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Plant Disease Detector'),
        actions: [
          Chip(
            label: Text(_isOnline ? 'Online' : 'Offline'),
            backgroundColor: _isOnline ? Colors.green : Colors.orange,
            labelStyle: TextStyle(color: Colors.white, fontSize: 12),
          ),
          SizedBox(width: 10),
          IconButton(
            icon: Icon(Icons.history),
            onPressed: () {
              Navigator.push(context,
                  MaterialPageRoute(builder: (context) => HistoryScreen()));
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Image Display
              Container(
                height: 300,
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: _image != null
                    ? ClipRRect(
                        borderRadius: BorderRadius.circular(12),
                        child: Image.file(_image!, fit: BoxFit.cover),
                      )
                    : Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.image, size: 80, color: Colors.grey),
                            SizedBox(height: 10),
                            Text('No image selected',
                                style: TextStyle(color: Colors.grey)),
                          ],
                        ),
                      ),
              ),
              SizedBox(height: 20),

              // Action Buttons
              Row(
                children: [
                  Expanded(
                    child: ElevatedButton.icon(
                      onPressed: _takePicture,
                      icon: Icon(Icons.camera_alt),
                      label: Text('Take Photo'),
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(vertical: 15),
                      ),
                    ),
                  ),
                  SizedBox(width: 10),
                  Expanded(
                    child: ElevatedButton.icon(
                      onPressed: _pickImage,
                      icon: Icon(Icons.photo_library),
                      label: Text('Gallery'),
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(vertical: 15),
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 20),

              // Loading Indicator
              if (_isLoading)
                Center(
                  child: Column(
                    children: [
                      CircularProgressIndicator(),
                      SizedBox(height: 10),
                      Text('Analyzing plant...'),
                    ],
                  ),
                ),

              // Results Display
              if (_prediction != null && !_isLoading)
                Card(
                  elevation: 4,
                  child: Padding(
                    padding: EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(Icons.info_outline, color: Colors.blue),
                            SizedBox(width: 10),
                            Text('Diagnosis',
                                style: TextStyle(
                                    fontSize: 20, fontWeight: FontWeight.bold)),
                          ],
                        ),
                        Divider(),
                        SizedBox(height: 10),
                        _buildResultRow('Disease',
                            _prediction!['predicted_class'].replaceAll('_', ' ')),
                        _buildResultRow('Confidence',
                            '${(_prediction!['confidence'] * 100).toStringAsFixed(1)}%'),
                        if (_prediction!['severity'] != null)
                          _buildResultRow('Severity', _prediction!['severity']),
                        _buildResultRow(
                            'Mode',
                            _prediction!['mode'] == 'online'
                                ? '🌐 Online'
                                : '📱 Offline'),
                        SizedBox(height: 15),

                        // Treatment Suggestions
                        if (_prediction!['treatment_suggestions'] != null)
                          _buildTreatmentSection(
                              _prediction!['treatment_suggestions']),

                        SizedBox(height: 10),
                        ElevatedButton.icon(
                          onPressed: () => _provideFeedback(),
                          icon: Icon(Icons.feedback),
                          label: Text('Provide Feedback'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.orange,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildResultRow(String label, String value) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 5),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label,
              style: TextStyle(fontWeight: FontWeight.w500, fontSize: 16)),
          Flexible(
            child: Text(value,
                style: TextStyle(fontSize: 16),
                textAlign: TextAlign.right,
                overflow: TextOverflow.ellipsis),
          ),
        ],
      ),
    );
  }

  Widget _buildTreatmentSection(List<dynamic> treatments) {
    return ExpansionTile(
      title: Text('Treatment Suggestions',
          style: TextStyle(fontWeight: FontWeight.bold)),
      children: treatments.map((treatment) {
        return ListTile(
          leading: Icon(
            treatment['type'] == 'organic' ? Icons.eco : Icons.science,
            color: treatment['type'] == 'organic' ? Colors.green : Colors.blue,
          ),
          title: Text(treatment['name']),
          subtitle: Text('${treatment['type']} - \$${treatment['cost_estimate']}'),
          trailing: Text('${(treatment['effectiveness'] * 100).toInt()}%'),
          onTap: () => _showTreatmentDetails(treatment),
        );
      }).toList(),
    );
  }

  void _showTreatmentDetails(Map<String, dynamic> treatment) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(treatment['name']),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Type: ${treatment['type']}'),
              SizedBox(height: 10),
              Text('Dosage: ${treatment['dosage']}'),
              SizedBox(height: 10),
              Text('Application: ${treatment['application_method']}'),
              SizedBox(height: 10),
              Text('Effectiveness: ${(treatment['effectiveness'] * 100).toInt()}%'),
              SizedBox(height: 10),
              Text('Side Effects:', style: TextStyle(fontWeight: FontWeight.bold)),
              ...List<Widget>.from(treatment['side_effects']
                  .map((effect) => Text('• $effect'))),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Close'),
          ),
        ],
      ),
    );
  }

  void _provideFeedback() {
    showDialog(
      context: context,
      builder: (context) => FeedbackDialog(prediction: _prediction!),
    );
  }
}