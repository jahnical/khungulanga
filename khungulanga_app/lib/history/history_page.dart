import 'package:flutter/material.dart';
import 'package:khungulanga_app/models/diagnosis.dart';
import 'package:khungulanga_app/repositories/diagnosis_repository.dart';
import 'package:khungulanga_app/diagnosis/diagnoses_list.dart';

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

  void _retryLoadDermatologists() {
    setState(() {
      _diagnosesFuture = DiagnosisRepository().fetchDiagnoses();
    });
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
            child: Padding(
              padding: const EdgeInsets.all(16),
              child:  Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'An error occurred while loading the diagnoses.',
                    style: Theme.of(context).textTheme.bodyMedium,
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 16.0),
                  ElevatedButton(
                    onPressed: _retryLoadDermatologists,
                    child: Text('Retry'),
                  ),
                ],
              ),
            ),
          );
        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text(
                  'Welcome to SmartSkin App!',
                  style: Theme.of(context).textTheme.headlineLarge?.apply(color: Theme.of(context).primaryColor),
                ),
                const SizedBox(height: 32),
                Text(
                  'Our app uses machine learning to diagnose skin diseases with high accuracy. Click the scan button to check your skin.',
                  style: Theme.of(context).textTheme.titleMedium,
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          );
        } else {
          final diagnoses = snapshot.data!;
          return DiagnosesList(diagnoses: diagnoses);
        }
      },
    );
  }
}
