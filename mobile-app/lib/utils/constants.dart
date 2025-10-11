class AppConstants {
  // API Configuration
  static const String API_URL = 'https://your-api.com';
  static const String API_VERSION = 'v1';
  
  // Model Configuration
  static const String MODEL_PATH = 'plant_disease_model.tflite';
  static const int IMAGE_SIZE = 128;
  static const int NUM_CLASSES = 3
  
  // Database Configuration
  static const String DB_NAME = 'plant_disease.db';
  static const int DB_VERSION = 1;
  
  // App Configuration
  static const String APP_NAME = 'Plant Disease Detector';
  static const int IMAGE_QUALITY = 85;
  static const int HISTORY_LIMIT = 50;
}