import 'package:flutter/material.dart';

class TreatmentList extends StatelessWidget {
  final List<dynamic> treatments;

  const TreatmentList({
    Key? key,
    required this.treatments,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (treatments.isEmpty) {
      return Card(
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Row(
            children: [
              Icon(Icons.info_outline, color: Colors.grey),
              SizedBox(width: 12),
              Expanded(
                child: Text(
                  'No treatment suggestions available for this disease.',
                  style: TextStyle(color: Colors.grey.shade600),
                ),
              ),
            ],
          ),
        ),
      );
    }

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ExpansionTile(
        leading: Icon(Icons.healing, color: Colors.green),
        title: Text(
          'Treatment Options (${treatments.length})',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
        ),
        subtitle: Text('Tap to view recommendations'),
        children: treatments
            .map((treatment) => TreatmentItem(treatment: treatment))
            .toList(),
      ),
    );
  }
}

class TreatmentItem extends StatelessWidget {
  final Map<String, dynamic> treatment;

  const TreatmentItem({Key? key, required this.treatment}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final isOrganic = treatment['type'] == 'organic';
    final effectiveness = (treatment['effectiveness'] as num).toDouble();

    return InkWell(
      onTap: () => _showTreatmentDetails(context),
      child: Container(
        padding: EdgeInsets.all(16),
        decoration: BoxDecoration(
          border: Border(
            top: BorderSide(color: Colors.grey.shade200),
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                // Type Icon
                Container(
                  padding: EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: isOrganic ? Colors.green.shade50 : Colors.blue.shade50,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    isOrganic ? Icons.eco : Icons.science,
                    color: isOrganic ? Colors.green : Colors.blue,
                    size: 24,
                  ),
                ),
                SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        treatment['name'],
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      SizedBox(height: 4),
                      Row(
                        children: [
                          _buildChip(
                            treatment['type'].toString().toUpperCase(),
                            isOrganic ? Colors.green : Colors.blue,
                          ),
                          SizedBox(width: 8),
                          Text(
                            '\${treatment['cost_estimate']}',
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.grey.shade700,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                // Effectiveness Badge
                Column(
                  children: [
                    CircularProgressIndicator(
                      value: effectiveness,
                      strokeWidth: 3,
                      backgroundColor: Colors.grey.shade200,
                      valueColor: AlwaysStoppedAnimation<Color>(
                        effectiveness > 0.8
                            ? Colors.green
                            : effectiveness > 0.6
                                ? Colors.orange
                                : Colors.red,
                      ),
                    ),
                    SizedBox(height: 4),
                    Text(
                      '${(effectiveness * 100).toInt()}%',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ],
            ),
            SizedBox(height: 12),
            Text(
              'Dosage: ${treatment['dosage']}',
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey.shade600,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildChip(String label, Color color) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Text(
        label,
        style: TextStyle(
          fontSize: 10,
          fontWeight: FontWeight.bold,
          color: color,
        ),
      ),
    );
  }

  void _showTreatmentDetails(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.7,
        minChildSize: 0.5,
        maxChildSize: 0.9,
        expand: false,
        builder: (context, scrollController) => SingleChildScrollView(
          controller: scrollController,
          padding: EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Handle bar
              Center(
                child: Container(
                  width: 40,
                  height: 4,
                  decoration: BoxDecoration(
                    color: Colors.grey.shade300,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              SizedBox(height: 20),

              // Title
              Text(
                treatment['name'],
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(height: 8),
              _buildChip(
                treatment['type'].toString().toUpperCase(),
                treatment['type'] == 'organic' ? Colors.green : Colors.blue,
              ),
              Divider(height: 32),

              // Details
              _buildDetailRow(
                Icons.medication,
                'Dosage',
                treatment['dosage'],
              ),
              _buildDetailRow(
                Icons.attach_money,
                'Estimated Cost',
                '\${treatment['cost_estimate']}',
              ),
              _buildDetailRow(
                Icons.timeline,
                'Effectiveness',
                '${(treatment['effectiveness'] * 100).toInt()}%',
              ),
              _buildDetailRow(
                Icons.agriculture,
                'Application',
                treatment['application_method'],
              ),

              SizedBox(height: 24),

              // Side Effects
              Text(
                'Side Effects',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(height: 12),
              ...List<Widget>.from(
                (treatment['side_effects'] as List).map(
                  (effect) => Padding(
                    padding: EdgeInsets.only(bottom: 8),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Icon(Icons.fiber_manual_record,
                            size: 8, color: Colors.grey),
                        SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            effect,
                            style: TextStyle(fontSize: 14),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),

              SizedBox(height: 24),

              // Close Button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => Navigator.pop(context),
                  child: Text('Close'),
                  style: ElevatedButton.styleFrom(
                    padding: EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildDetailRow(IconData icon, String label, String value) {
    return Padding(
      padding: EdgeInsets.only(bottom: 16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 20, color: Colors.blue),
          SizedBox(width: 12),
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
                SizedBox(height: 4),
                Text(
                  value,
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}