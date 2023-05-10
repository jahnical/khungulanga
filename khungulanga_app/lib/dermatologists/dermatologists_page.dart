import 'package:flutter/material.dart';
import 'package:khungulanga_app/dermatologists/dermatologists_list.dart';
import 'package:khungulanga_app/models/dermatologist.dart';
import 'package:khungulanga_app/models/diagnosis.dart';

class DermatologistsPage extends StatelessWidget {
  final List<double> userLocation = [0.0, 0.0];
  final Diagnosis? diagnosis;

  DermatologistsPage({this.diagnosis});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dermatologists'),
      ),
      body: DermatologistList(
        userLocation: userLocation,
        diagnosis: diagnosis,
      ),
    );
  }
}