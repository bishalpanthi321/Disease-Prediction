class FeedbackModel {
  final String id;
  final String predictionId;
  final String correctClass;
  final String? comments;
  final String timestamp;
  final bool synced;

  FeedbackModel({
    required this.id,
    required this.predictionId,
    required this.correctClass,
    this.comments,
    required this.timestamp,
    this.synced = false,
  });

  // Convert from database Map
  factory FeedbackModel.fromMap(Map<String, dynamic> map) {
    return FeedbackModel(
      id: map['id'] as String,
      predictionId: map['prediction_id'] as String,
      correctClass: map['correct_class'] as String,
      comments: map['comments'] as String?,
      timestamp: map['timestamp'] as String,
      synced: (map['synced'] as int) == 1,
    );
  }

  // Convert to database Map
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'prediction_id': predictionId,
      'correct_class': correctClass,
      'comments': comments,
      'timestamp': timestamp,
      'synced': synced ? 1 : 0,
    };
  }

  // Display-friendly class name
  String get displayClassName => correctClass.replaceAll('_', ' ');
}