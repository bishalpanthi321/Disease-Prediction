import 'package:flutter/material.dart';
import 'dart:io';
import '../services/database_helper.dart';

// History Screen
class HistoryScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Prediction History'),
      ),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: DatabaseHelper.instance.getAllPredictions(limit: 50),
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return Center(child: CircularProgressIndicator());
          }

          var predictions = snapshot.data!;

          if (predictions.isEmpty) {
            return Center(child: Text('No predictions yet'));
          }

          return ListView.builder(
            itemCount: predictions.length,
            itemBuilder: (context, index) {
              var pred = predictions[index];
              return Card(
                margin: EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                child: ListTile(
                  leading: CircleAvatar(
                    backgroundImage: File(pred['image_path']).existsSync()
                        ? FileImage(File(pred['image_path']))
                        : null,
                    child: !File(pred['image_path']).existsSync()
                        ? Icon(Icons.image_not_supported)
                        : null,
                  ),
                  title: Text(pred['predicted_class'].replaceAll('_', ' ')),
                  subtitle: Text(
                      'Confidence: ${(pred['confidence'] * 100).toStringAsFixed(1)}%\n${pred['timestamp']}'),
                  trailing: Icon(
                    pred['synced'] == 1 ? Icons.cloud_done : Icons.cloud_off,
                    color: pred['synced'] == 1 ? Colors.green : Colors.grey,
                  ),
                  isThreeLine: true,
                ),
              );
            },
          );
        },
      ),
    );
  }
}