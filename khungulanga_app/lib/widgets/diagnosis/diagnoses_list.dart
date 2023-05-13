import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:khungulanga_app/blocs/diagnosis_bloc/diagnosis_bloc.dart';
import 'package:khungulanga_app/models/diagnosis.dart';
import 'package:khungulanga_app/util/common.dart';
import 'package:khungulanga_app/api_connection/endpoints.dart';
import 'package:khungulanga_app/widgets/diagnosis/diagnosis_page.dart';


class DiagnosesList extends StatelessWidget {
  final List<Diagnosis> diagnoses;

  const DiagnosesList({Key? key, required this.diagnoses}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return BlocListener<DiagnosisBloc, DiagnosisState>(
      listener: (context, state) {
        log(state.toString());
        if (state is DiagnosisDeletingError) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('An error occurred while deleting the diagnosis.'),
            ),
          );
        } else if (state is ConfirmingDiagnosisDelete) {
          _confirmDelete(state.diagnosis, context, context.read<DiagnosisBloc>());
        }
      },
      child: BlocBuilder<DiagnosisBloc, DiagnosisState>(
          builder: (context, state) {
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
                                    style: const TextStyle(
                                      fontWeight: FontWeight.bold,
                                      fontSize: 18,
                                    ),
                                  ),
                                  const SizedBox(height: 8),
                                  Text(
                                    '${(diagnosis.predictions[0].probability * 100).toInt()}% probability',
                                    style: const TextStyle(
                                      fontWeight: FontWeight.w400,
                                      fontSize: 14,
                                    ),
                                  ),
                                  const SizedBox(height: 8),
                                  Text(
                                    diagnosis.date.toString(),
                                    style: const TextStyle(
                                      fontWeight: FontWeight.w400,
                                      fontSize: 12,
                                      color: Colors.grey,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                          Container(
                            child: state is DiagnosisDeleting && state.diagnosis.id == diagnosis.id? const SizedBox(width: 24, height: 24, child: CircularProgressIndicator(),)
                                : IconButton(
                              icon: const Icon(
                                Icons.delete,
                                color: Colors.redAccent,
                              ),
                              onPressed: () {
                                context.read<DiagnosisBloc>().add(DeleteDiagnosisPressed(diagnosis));
                              },
                            ),
                          )
                        ],
                      ),
                    ),
                  ),
                );
              },
            );
          },
        ),
    );
  }

  void _confirmDelete(Diagnosis diagnosis, BuildContext context, DiagnosisBloc bloc) async {
    final confirmed = await showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Diagnosis'),
        content: const Text('Are you sure you want to delete this diagnosis?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('CANCEL'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.of(context).pop(true),
            style: ElevatedButton.styleFrom(
              primary: Theme.of(context).errorColor,
            ),
            child: const Text('DELETE'),
          ),
        ],
      ),
    );

    if (confirmed != null && confirmed) {
      bloc.add(DeleteDiagnosis(diagnosis));
    }
  }
}


