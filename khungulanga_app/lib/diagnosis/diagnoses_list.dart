import 'package:flutter/material.dart';
import 'package:khungulanga_app/models/diagnosis.dart';
import 'package:khungulanga_app/diagnosis/diagnosis_page.dart';

import '../repositories/diagnosis_repository.dart';
import '../util/common.dart';
import '../util/endpoints.dart';

class DiagnosesList extends StatefulWidget {
  final List<Diagnosis> diagnoses;

  const DiagnosesList({Key? key, required this.diagnoses}) : super(key: key);

  @override
  State<StatefulWidget> createState() {
    return DiagnosisListState(diagnoses);
  }
}

class DiagnosisListState extends State<DiagnosesList>  {
  bool _loading = false;
  final List<Diagnosis> diagnoses;

  DiagnosisListState(this.diagnoses);

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
              padding: const EdgeInsets.all(8.0),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SizedBox(
                    height: 72,
                    width: 72,
                    child: Image.network(
                      BASE_URL + diagnosis.imageUrl,
                      fit: BoxFit.cover,
                    ),
                  ),
                  SizedBox(width: 16),
                  Expanded(
                    child: Padding(
                      padding: const EdgeInsets.only(left: 8.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            toTitleCase(diagnosis.predictions[0].disease.name),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
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
                              fontSize: 14,
                            ),
                          ),
                          SizedBox(height: 8),
                          Text(
                            diagnosis.date.toString(),
                            style: TextStyle(
                              fontWeight: FontWeight.w400,
                              fontSize: 12,
                              color: Colors.grey,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  IconButton(
                    icon: Icon(
                      Icons.delete,
                      color: Theme.of(context).errorColor,
                    ),
                    onPressed: () {
                      _onDeleteClicked(diagnosis, context);
                    },
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  void _onDeleteClicked(Diagnosis _diagnosis, BuildContext context) async {
    final confirmed = await showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Delete Diagnosis'),
        content: Text('Are you sure you want to delete this diagnosis?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: Text('CANCEL'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.of(context).pop(true),
            style: ElevatedButton.styleFrom(
              primary: Theme.of(context).errorColor,
            ),
            child: Text('DELETE'),
          ),
        ],
      ),
    );

    if (confirmed != null && confirmed) {
      setState(() {
        _loading = true;
      });

      final result = await DiagnosisRepository().delete(_diagnosis.id);

      setState(() {
        _loading = false;

        if (result == true) {
          diagnoses.remove(_diagnosis);
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('An error occurred while deleting the diagnosis.'),
            ),
          );
        }
      });
    }
  }
}
