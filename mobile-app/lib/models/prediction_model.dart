class PredictionModel {
  final String id;
  final String timestamp;
  final String predictedClass;
  final double confidence;
  final String imagePath;
  final String severity;
  final bool synced;
  final Map<String, dynamic>? metadata;
  final Map<String, double>? probabilities;
  final List<Treatment>? treatments;

  PredictionModel({
    required this.id,
    required this.timestamp,
    required this.predictedClass,
    required this.confidence,
    required this.imagePath,
    this.severity = 'unknown',
    this.synced = false,
    this.metadata,
    this.probabilities,
    this.treatments,
  });

  // Convert from database Map
  factory PredictionModel.fromMap(Map<String, dynamic> map) {
    return PredictionModel(
      id: map['id'] as String,
      timestamp: map['timestamp'] as String,
      predictedClass: map['predicted_class'] as String,
      confidence: map['confidence'] as double,
      imagePath: map['image_path'] as String,
      severity: map['severity'] as String? ?? 'unknown',
      synced: (map['synced'] as int) == 1,
      metadata: map['metadata'] != null 
          ? Map<String, dynamic>.from(map['metadata']) 
          : null,
    );
  }

  // Convert to database Map
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'timestamp': timestamp,
      'predicted_class': predictedClass,
      'confidence': confidence,
      'image_path': imagePath,
      'severity': severity,
      'synced': synced ? 1 : 0,
      'metadata': metadata.toString(),
    };
  }

  // Display-friendly disease name
  String get displayName => predictedClass.replaceAll('_', ' ');

  // Confidence as percentage
  String get confidencePercentage => '${(confidence * 100).toStringAsFixed(1)}%';

  // Check if healthy
  bool get isHealthy => predictedClass.toLowerCase().contains('healthy');

  // Get severity color
  String get severityColor {
    switch (severity.toLowerCase()) {
      case 'healthy':
        return '#4CAF50'; // Green
      case 'mild':
        return '#FFC107'; // Amber
      case 'moderate':
        return '#FF9800'; // Orange
      case 'severe':
        return '#F44336'; // Red
      case 'critical':
        return '#D32F2F'; // Dark Red
      default:
        return '#9E9E9E'; // Grey
    }
  }
}

class Treatment {
  final String name;
  final String type;
  final String dosage;
  final double costEstimate;
  final double effectiveness;
  final List<String> sideEffects;
  final String applicationMethod;

  Treatment({
    required this.name,
    required this.type,
    required this.dosage,
    required this.costEstimate,
    required this.effectiveness,
    required this.sideEffects,
    required this.applicationMethod,
  });

  factory Treatment.fromJson(Map<String, dynamic> json) {
    return Treatment(
      name: json['name'] as String,
      type: json['type'] as String,
      dosage: json['dosage'] as String,
      costEstimate: (json['cost_estimate'] as num).toDouble(),
      effectiveness: (json['effectiveness'] as num).toDouble(),
      sideEffects: List<String>.from(json['side_effects'] as List),
      applicationMethod: json['application_method'] as String,
    );
  }

  String get effectivenessPercentage => '${(effectiveness * 100).toInt()}%';
}