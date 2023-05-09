import 'package:flutter/material.dart';
import 'package:smartskin_app/models/diagnosis.dart';
import 'package:smartskin_app/repositories/diagnosis_repository.dart';
import 'package:smartskin_app/diagnosis/diagnoses_list.dart';

class HistoryPage extends StatefulWidget {
  const HistoryPage({Key? key}) : super(key: key);

  @override
  _HistoryPageState createState() => _HistoryPageState();
}

class _HistoryPageState extends State<HistoryPage> {
  late Future<List<Diagnosis>> _diagnosesFuture;

  @override
  void initState() {
    super.initState();
    _diagnosesFuture = DiagnosisRepository().fetchDiagnoses();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Diagnosis>>(
      future: _diagnosesFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Center(
            child: Text(
              'An error occurred while loading the diagnoses.',
              style: Theme.of(context).textTheme.headline6,
              textAlign: TextAlign.center,
            ),
          );
        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Welcome to SmartSkin App!',
                style: Theme.of(context).textTheme.headline5,
              ),
              const SizedBox(height: 16),
              Text(
                'Our app uses machine learning to diagnose skin diseases with high accuracy. Click the scan button to check your skin.',
                style: Theme.of(context).textTheme.subtitle1,
                textAlign: TextAlign.center,
              ),
            ],
          );
        } else {
          final diagnoses = snapshot.data!;
          return DiagnosisList(diagnoses: diagnoses);
        }
      },
    );
  }
}
