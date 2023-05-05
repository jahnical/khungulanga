
import 'package:flutter/material.dart';

class DiagnosisPage extends StatelessWidget {
  List<dynamic>? predictions;

  DiagnosisPage({super.key});

  @override
  Widget build(BuildContext context) {
    predictions = ModalRoute.of(context)!.settings.arguments as List<dynamic>;
    return Scaffold(
      appBar: AppBar(
        title: Text('Diagnosis Results'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              'The predicted diagnosis is:',
            ),
            Text(
              '${predictions}',
              style: TextStyle(fontSize: 24),
            ),
          ],
        ),
      ),
    );
  }
}
