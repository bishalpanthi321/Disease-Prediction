import 'package:flutter/material.dart';

class ResultCard extends StatelessWidget{
    final String predictionClass;
    final double confidence; 
    final String? severity;
    final String mode;
    final VoidCallback? onFeedback;


    const ResultCard({
        Key? key,
        required this.predictionClass,
        required this.confidence,
        this.severity,
        required this.mode, 
        this.onFeedback
    }) : super (key: key);


    Color _getSeverityColor() {
        if (severity == null ) return Colors.grey;

        switch(severity!.toLowerCase()) {
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


    IconData _getSeverityColor() {
        if (severity == null) return Icons.help.outline;
        switch (severity!.toLowerCase()){
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
            shape: RoundRectangleBorder(borderRadius: BorderRadius.circular(12)),

            child: Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                    crossAxisAlignment: crossAxisAlignment.start,

                    children: [
                        Row(
                            children: [
                                Icon(Icons.medical_services, color: Colors.blue, size: 28),
                                SizedBox(width: 12),
                                Text (
                                    'Diagnosis Results',
                                    style: TextStyle (
                                        fontSize: 20,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.blue.shade900, 
                                    ), 
                                ), 
                            ], 
                        ),

                        Divider height(:24, thickness: 1),

                        _buildResultRow(
                            'Disease',
                            predictedClass.replaceAll('_',' '),
                            Icons.coronavirus,
                            Colors.blue, 
                        ), 

                        _buildConfidenceBar(), 

                        if(severity != null)
                        _buildResultRow(
                            'Severity',
                            severity!.toUpperCase(),
                            _getSeverityIcon(),
                            _getSeverityColor(), 
                        ), 

                        _buildResultRow(
                            'Analysis Mode',
                            mode == 'online' ? '🌐 Online' : '📱 Offline', 
                            mode == 'online' ? Icons.cloud_done : Icons.phone_android, 
                            mode == 'online' ? Colors.green : Colors.orange, 
                        ), 


                        if(onFeedback != null) ...[
                            SizedBox(height:16),
                            SizedBox(
                                width: double.infinity,
                                child: ElevatedButton.icon(
                                    onPressed: onFeedback,
                                    icon: Icon(Icons.feedback), 
                                    style: ElevatedButton.styleFrom(
                                        backgroundColor: Colors.orange,
                                        padding: EdgeInsets.symmetric(vertical: 12),
                                        shape: RoundRectangleBorder(
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


    


}