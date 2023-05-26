import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:dermatologist_app/models/diagnosis.dart';
import 'package:dermatologist_app/api_connection/endpoints.dart';

class DiagnosisPage extends StatelessWidget {
  final Diagnosis diagnosis;

  const DiagnosisPage({Key? key, required this.diagnosis}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Diagnosis'),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Column(
              children: [
                Container(
                  height: 200,
                  width: double.infinity,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(1.0),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.2),
                        offset: Offset(0.0, 2.0),
                        blurRadius: 4.0,
                      ),
                    ],
                  ),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(8.0),
                    child: Image.network(
                      BASE_URL + diagnosis.imageUrl,
                      fit: BoxFit.cover,
                    ),
                  ),
                ),
                SizedBox(height: 16),
                Text(
                  diagnosis.predictions[0].disease.name.toUpperCase(),
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: Colors.lightBlueAccent,
                  ),
                ),
                SizedBox(height: 8),
                Text(
                  '${(diagnosis.predictions[0].probability * 100).toInt()}% Probability',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.grey,
                  ),
                ),
                SizedBox(height: 16),
                Container(
                  padding:
                  EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                  decoration: BoxDecoration(
                    color: Colors.lightBlueAccent.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(8.0),
                  ),
                  child: Text(
                    diagnosis.predictions[0].disease.description,
                    textAlign: TextAlign.start,
                    style: TextStyle(fontSize: 16),
                  ),
                ),
                SizedBox(height: 16.0),
                ListTile(
                  leading: Icon(
                    Icons.medical_services,
                    color: Colors.blue,
                  ),
                  title: Text(
                    diagnosis.predictions[0].disease.treatments[0].title,
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  subtitle: Text(diagnosis
                      .predictions[0].disease.treatments[0].description),
                ),
              ],
            ),
            SizedBox(height: 24),
            Column(
              children: [
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
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w400,
                        color: Colors.redAccent,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
              ],
            ),
            SizedBox(height: 16),
            Divider(
              thickness: 2.0,
              height: 16.0,
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(8.0),
                        decoration: BoxDecoration(
                          color: Colors.blue[50],
                          borderRadius: BorderRadius.circular(8.0),
                        ),
                        child: Icon(
                          Icons.help_outline,
                          size: 32,
                          color: Colors.green,
                        ),
                      ),
                      SizedBox(width: 16),
                      Text(
                        'Other possible diagnoses:',
                        style: TextStyle(
                            fontSize: 18, fontWeight: FontWeight.bold),
                        textAlign: TextAlign.start,
                      ),
                    ],
                  ),
                  SizedBox(height: 4.0),
                  ListView.builder(
                    shrinkWrap: true,
                    physics: NeverScrollableScrollPhysics(),
                    itemCount: diagnosis.predictions.length - 1,
                    itemBuilder: (context, index) {
                      return Column(
                        children: [
                          SizedBox(height: 8),
                          Card(
                            elevation: 2.0,
                            child: ListTile(
                              leading: Icon(
                                Icons.local_hospital,
                                color: Colors.blue,
                              ),
                              title: Text(
                                diagnosis
                                    .predictions[index + 1].disease.name
                                    .toUpperCase(),
                                style: const TextStyle(
                                    fontWeight: FontWeight.bold),
                              ),
                              subtitle: Text(
                                _getEllipsizedDescription(diagnosis
                                    .predictions[index + 1]
                                    .disease
                                    .description),
                              ),
                              trailing: Container(
                                padding: EdgeInsets.symmetric(
                                    horizontal: 12, vertical: 6),
                                decoration: BoxDecoration(
                                  color: Colors.blue,
                                  borderRadius: BorderRadius.circular(16.0),
                                ),
                                child: Text(
                                  '${(diagnosis.predictions[index + 1].probability * 100).toInt()}%',
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    color: Colors.white,
                                  ),
                                ),
                              ),
                            ),
                          ),
                          SizedBox(height: 8),
                          if (index < diagnosis.predictions.length - 2)
                            Divider(
                              color: Colors.grey[300],
                              height: 1,
                              thickness: 1,
                            ),
                        ],
                      );
                    },
                  ),
                ],
              ),
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
