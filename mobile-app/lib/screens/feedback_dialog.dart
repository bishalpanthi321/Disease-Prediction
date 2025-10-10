import 'package:flutter/material.dart';
import '../services/database_helper.dart';
import '../services/model_service.dart';

// Feedback Dialog
class FeedbackDialog extends StatefulWidget {
  final Map<String, dynamic> prediction;

  FeedbackDialog({required this.prediction});

  @override
  _FeedbackDialogState createState() => _FeedbackDialogState();
}

class _FeedbackDialogState extends State<FeedbackDialog> {
  String? _selectedClass;
  TextEditingController _commentsController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text('Provide Feedback'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text('Is the diagnosis correct?'),
          SizedBox(height: 10),
          DropdownButton<String>(
            hint: Text('Select correct disease'),
            value: _selectedClass,
            isExpanded: true,
            items: ModelService.instance.labels!
                .map((label) => DropdownMenuItem(
                      value: label,
                      child: Text(label.replaceAll('_', ' ')),
                    ))
                .toList(),
            onChanged: (value) {
              setState(() {
                _selectedClass = value;
              });
            },
          ),
          SizedBox(height: 10),
          TextField(
            controller: _commentsController,
            decoration: InputDecoration(
              labelText: 'Additional comments',
              border: OutlineInputBorder(),
            ),
            maxLines: 3,
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: () async {
            // Save feedback
            await DatabaseHelper.instance.insertFeedback({
              'id': DateTime.now().millisecondsSinceEpoch.toString(),
              'prediction_id': widget.prediction['prediction_id'] ?? 'offline',
              'correct_class': _selectedClass ?? widget.prediction['predicted_class'],
              'comments': _commentsController.text,
              'timestamp': DateTime.now().toIso8601String(),
              'synced': 0,
            });
            Navigator.pop(context);
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Thank you for your feedback!')),
            );
          },
          child: Text('Submit'),
        ),
      ],
    );
  }
}