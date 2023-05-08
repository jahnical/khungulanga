import 'dart:developer';
import 'dart:ffi';

import 'package:flutter/material.dart';
import 'package:smartskin_app/models/dermatologist.dart';
import 'package:smartskin_app/models/diagnosis.dart';
import 'package:smartskin_app/repositories/dermatologist_repository.dart';

class DermatologistsPage extends StatefulWidget {
  final List<Double> userLocation = List.from([0.0, 0.0]);
  final Diagnosis? diagnosis;

  DermatologistsPage({this.diagnosis});

  @override
  _DermatologistsPageState createState() => _DermatologistsPageState();
}

class _DermatologistsPageState extends State<DermatologistsPage> {
  List<Dermatologist> dermatologists = [];

  @override
  void initState() {
    super.initState();
    _loadDermatologists();
  }

  void _loadDermatologists() async {
    try {
      dermatologists = await DermatologistRepository().getNearbyDermatologists(
          widget.userLocation[0], widget.userLocation[1]);
      setState(() {});
    } catch (e) {
      log('Failed to load dermatologists: $e');
    }
  }

  void _bookAppointment(Dermatologist dermatologist) {
    // Code to book appointment with the selected dermatologist
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dermatologists'),
      ),
      body: ListView.builder(
        itemCount: dermatologists.length,
        itemBuilder: (BuildContext context, int index) {
          final dermatologist = dermatologists[index];
          return ListTile(
            title: Text(dermatologist.qualification),
            subtitle: Text(dermatologist.clinic),
            trailing: IconButton(
              icon: Icon(Icons.book),
              onPressed: () => _bookAppointment(dermatologist),
            ),
            onTap: () {
              // Code to show dermatologist details
            },
          );
        },
      ),
    );
  }
}
