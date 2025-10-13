import 'package:flutter/material.dart';

class ResultCard extends StatelessWidget {
  final String predictedClass;
  final double confidence;
  final String? severity;
  final String mode;
  final VoidCallback? onFeedback;

  const ResultCard({
    Key? key,
    required this.predictedClass,
    required this.confidence,
    this.severity,
    required this.mode,
    this.onFeedback,
  }) : super(key: key);

  Color _getSeverityColor() {
    if (severity == null) return Colors.grey;
    switch (severity!.toLowerCase()) {
      case 'healthy':
        return Colors.green;
      case 'mild':
        return Colors.amber;
      case 'moderate':
        return Colors.orange;
      case 'severe':
        return Colors.red;
      case 'critical':
        return Colors.red.shade900;
      default:
        return Colors.grey;
    }
  }

  IconData _getSeverityIcon() {
    if (severity == null) return Icons.help_outline;
    switch (severity!.toLowerCase()) {
      case 'healthy':
        return Icons.check_circle;
      case 'mild':
        return Icons.warning_amber;
      case 'moderate':
        return Icons.warning;
      case 'severe':
        return Icons.error;
      case 'critical':
        return Icons.dangerous;
      default:
        return Icons.help_outline;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Row(
              children: [
                Icon(Icons.medical_services, color: Colors.blue, size: 28),
                SizedBox(width: 12),
                Text(
                  'Diagnosis Results',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Colors.blue.shade900,
                  ),
                ),
              ],
            ),
            Divider(height: 24, thickness: 1),

            // Disease Name
            _buildResultRow(
              'Disease',
              predictedClass.replaceAll('_', ' '),
              Icons.coronavirus,
              Colors.blue,
            ),

            // Confidence
            _buildConfidenceBar(),

            // Severity
            if (severity != null)
              _buildResultRow(
                'Severity',
                severity!.toUpperCase(),
                _getSeverityIcon(),
                _getSeverityColor(),
              ),

            // Mode
            _buildResultRow(
              'Analysis Mode',
              mode == 'online' ? '🌐 Online' : '📱 Offline',
              mode == 'online' ? Icons.cloud_done : Icons.phone_android,
              mode == 'online' ? Colors.green : Colors.orange,
            ),

            // Feedback Button
            if (onFeedback != null) ...[
              SizedBox(height: 16),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: onFeedback,
                  icon: Icon(Icons.feedback),
                  label: Text('Provide Feedback'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.orange,
                    padding: EdgeInsets.symmetric(vertical: 12),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildResultRow(String label, String value, IconData icon, Color color) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Icon(icon, size: 20, color: color),
          SizedBox(width: 8),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey.shade600,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                SizedBox(height: 2),
                Text(
                  value,
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: Colors.black87,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildConfidenceBar() {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Icon(Icons.speed, size: 20, color: Colors.blue),
                  SizedBox(width: 8),
                  Text(
                    'Confidence',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey.shade600,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
              Text(
                '${(confidence * 100).toStringAsFixed(1)}%',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.blue.shade700,
                ),
              ),
            ],
          ),
          SizedBox(height: 8),
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: LinearProgressIndicator(
              value: confidence,
              minHeight: 12,
              backgroundColor: Colors.grey.shade200,
              valueColor: AlwaysStoppedAnimation<Color>(
                confidence > 0.8
                    ? Colors.green
                    : confidence > 0.6
                        ? Colors.orange
                        : Colors.red,
              ),
            ),
          ),
        ],
      ),
    );
  }
}