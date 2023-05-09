import 'package:flutter/material.dart';
import 'package:smartskin_app/models/diagnosis.dart';
import 'package:smartskin_app/diagnosis/diagnosis_page.dart';

class DiagnosesList extends StatelessWidget {
  final List<Diagnosis> diagnoses;

  const DiagnosesList({Key? key, required this.diagnoses}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: diagnoses.length,
      itemBuilder: (context, index) {
        final diagnosis = diagnoses[index];
        return Card(
          child: InkWell(
            onTap: () {
              Navigator.of(context).push(MaterialPageRoute(
                builder: (context) => DiagnosisPage(diagnosis: diagnosis),
              ));
            },
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Image.network(
                    diagnosis.imageUrl,
                    height: 80,
                    width: 80,
                    fit: BoxFit.cover,
                  ),
                  SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          diagnosis.predictions[0].disease.name.toUpperCase(),
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 18,
                          ),
                        ),
                        SizedBox(height: 8),
                        Text(
                          '${(diagnosis.predictions[0].probability * 100).toInt()}% probability',
                          style: TextStyle(
                            fontWeight: FontWeight.w400,
                            fontSize: 16,
                          ),
                        ),
                        SizedBox(height: 8),
                        Text(
                          diagnosis.date.toString(),
                          style: TextStyle(
                            fontWeight: FontWeight.w400,
                            fontSize: 14,
                            color: Colors.grey,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}
