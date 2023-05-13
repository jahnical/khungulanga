import 'package:flutter/material.dart';
import 'package:khungulanga_app/models/disease.dart';

class DiseaseDetailPage extends StatelessWidget {
  final Disease disease;

  const DiseaseDetailPage({super.key, required this.disease});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(disease.name),
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    return SingleChildScrollView(
      padding: EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            disease.name,
            style: TextStyle(
              fontSize: 24.0,
              fontWeight: FontWeight.bold,
            ),
          ),
          SizedBox(height: 16.0),
          Text(
            disease.description,
            style: TextStyle(
              fontSize: 16.0,
            ),
          ),
          SizedBox(height: 16.0),
          Text(
            'Severity: ${disease.severity}',
            style: TextStyle(
              fontSize: 16.0,
            ),
          ),
          SizedBox(height: 16.0),
          Text(
            'Treatments:',
            style: TextStyle(
              fontSize: 16.0,
              fontWeight: FontWeight.bold,
            ),
          ),
          SizedBox(height: 8.0),
          ListView.builder(
            shrinkWrap: true,
            itemCount: disease.treatments.length,
            itemBuilder: (context, index) {
              final treatment = disease.treatments[index];
              return ListTile(
                title: Text(treatment.title),
                subtitle: Text(treatment.description),
              );
            },
          ),
        ],
      ),
    );
  }
}