import 'package:flutter/material.dart';

class TreatmentList extends StatelessWidget {
  final List<Map<String, dynamic>> treatments;

  const TreatmentList({
    Key? key,
    required this.treatments,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (treatments.isEmpty) {
      return Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              const Icon(Icons.info_outline, color: Colors.grey),
              const SizedBox(width: 12),
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
        leading: const Icon(Icons.healing, color: Colors.green),
        title: Text(
          'Treatment Options (${treatments.length})',
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
        ),
        subtitle: const Text('Tap to view recommendations'),
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
    final isOrganic = treatment['type']?.toString().toLowerCase() == 'organic';
    final effectiveness =
        (treatment['effectiveness'] as num?)?.toDouble() ?? 0.0;
    final costEstimate = treatment['cost_estimate']?.toString() ?? 'N/A';
    final dosage = treatment['dosage']?.toString() ?? 'N/A';
    final application = treatment['application_method']?.toString() ?? 'N/A';
    final sideEffects = (treatment['side_effects'] as List<dynamic>?)
            ?.map((e) => e.toString())
            .toList() ??
        [];

    return InkWell(
      onTap: () => _showTreatmentDetails(
        context,
        treatmentName: treatment['name']?.toString() ?? 'Unknown',
        isOrganic: isOrganic,
        dosage: dosage,
        cost: costEstimate,
        effectiveness: effectiveness,
        application: application,
        sideEffects: sideEffects,
      ),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          border: Border(
            top: BorderSide(color: Colors.grey.shade200),
          ),
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Type Icon
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color:
                    isOrganic ? Colors.green.shade50 : Colors.blue.shade50,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(
                isOrganic ? Icons.eco : Icons.science,
                color: isOrganic ? Colors.green : Colors.blue,
                size: 24,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    treatment['name']?.toString() ?? 'Unknown Treatment',
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Row(
                    children: [
                      _buildChip(
                          treatment['type']?.toString().toUpperCase() ?? 'N/A',
                          isOrganic ? Colors.green : Colors.blue),
                      const SizedBox(width: 8),
                      Text(
                        costEstimate,
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
                const SizedBox(height: 4),
                Text(
                  '${(effectiveness * 100).toInt()}%',
                  style: const TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildChip(String label, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
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

  void _showTreatmentDetails(
    BuildContext context, {
    required String treatmentName,
    required bool isOrganic,
    required String dosage,
    required String cost,
    required double effectiveness,
    required String application,
    required List<String> sideEffects,
  }) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.7,
        minChildSize: 0.5,
        maxChildSize: 0.9,
        expand: false,
        builder: (context, scrollController) => SingleChildScrollView(
          controller: scrollController,
          padding: const EdgeInsets.all(24),
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
              const SizedBox(height: 20),
              // Title
              Text(
                treatmentName,
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              _buildChip(
                isOrganic ? 'ORGANIC' : 'CHEMICAL',
                isOrganic ? Colors.green : Colors.blue,
              ),
              const Divider(height: 32),
              // Details
              _buildDetailRow(Icons.medication, 'Dosage', dosage),
              _buildDetailRow(Icons.attach_money, 'Estimated Cost', cost),
              _buildDetailRow(
                  Icons.timeline, 'Effectiveness', '${(effectiveness * 100).toInt()}%'),
              _buildDetailRow(Icons.agriculture, 'Application', application),
              const SizedBox(height: 24),
              // Side Effects
              const Text(
                'Side Effects',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 12),
              ...sideEffects.map(
                (effect) => Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.fiber_manual_record, size: 8, color: Colors.grey),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          effect,
                          style: const TextStyle(fontSize: 14),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),
              // Close Button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Close'),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
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
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 20, color: Colors.blue),
          const SizedBox(width: 12),
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
                const SizedBox(height: 4),
                Text(
                  value,
                  style: const TextStyle(
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