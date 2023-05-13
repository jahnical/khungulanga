import 'package:flutter/material.dart';
import 'package:khungulanga_app/models/diagnosis.dart';
import 'package:khungulanga_app/api_connection/endpoints.dart';
import 'package:khungulanga_app/widgets/dermatologists/dermatologists_page.dart';

class DiagnosisPage extends StatelessWidget {
  final Diagnosis diagnosis;

  const DiagnosisPage({Key? key, required this.diagnosis}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Diagnosis Results'),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Image.network(
              BASE_URL + diagnosis.imageUrl,
              fit: BoxFit.cover,
              height: 200,
              width: double.infinity,
            ),
            SizedBox(height: 16),
            Text(
              diagnosis.predictions[0].disease.name.toUpperCase(),
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Colors.lightBlueAccent,
              ),
            ),
            SizedBox(height: 8),
            Text(
              '${(diagnosis.predictions[0].probability * 100).toInt()}% Probability',
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: Colors.grey,
              ),
            ),
            SizedBox(height: 16),
            Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                decoration: BoxDecoration(
                  color: Colors.lightBlueAccent.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(8.0),
                ),
                child: Text(
                  diagnosis.predictions[0].disease.description,
                  textAlign: TextAlign.start,
                  style: const TextStyle(fontSize: 16),
                ),
              ),
            ),
            SizedBox(height: 24),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Container(
                padding: const EdgeInsets.all(16.0),
                decoration: BoxDecoration(
                  color: Colors.redAccent.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: Colors.redAccent),
                ),
                child: Text(
                  'Note: This should not be considered a final diagnosis or used in place of a dermatologist.',
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w400,
                    color: Colors.redAccent,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
            SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) => DermatologistsPage(
                      diagnosis: diagnosis,
                    ),
                  ),
                );
              },
              icon: Icon(Icons.phone),
              label: Text('Contact a Dermatologist'),
              style: ElevatedButton.styleFrom(
                primary: Colors.lightBlueAccent,
                padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8.0),
                ),
              ),
            ),
            SizedBox(height: 16),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                children: [
                  Icon(
                    Icons.help_outline,
                    size: 32,
                    color: Colors.grey,
                  ),
                  SizedBox(width: 16),
                  Text(
                    'Other possible diagnoses:',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    textAlign: TextAlign.start,
                  ),
                ],
              ),
            ),
            SizedBox(height: 16),
            ListView.builder(
              shrinkWrap: true,
              physics: NeverScrollableScrollPhysics(),
              itemCount: diagnosis.predictions.length - 1,
              itemBuilder: (context, index) {
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    ListTile(
                      title: Text(
                        diagnosis.predictions[index + 1].disease.name.toUpperCase(),
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: Text(
                        _getEllipsizedDescription(diagnosis.predictions[index + 1].disease.description),
                      ),
                      trailing: Text(
                        '${(diagnosis.predictions[index + 1].probability * 100).toInt()}%',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ),
                    SizedBox(height: 8),
                  ],
                );
              },
            ),
            SizedBox(height: 16),
          ],
        ),
      ),
    );
  }

  String _getEllipsizedDescription(String description) {
    if (description.length > 100) {
      return description.substring(0, 100) + '...';
    } else {
      return description;
    }
  }
}
