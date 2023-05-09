import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:smartskin_app/models/dermatologist.dart';
import 'package:smartskin_app/models/diagnosis.dart';
import 'package:smartskin_app/repositories/dermatologist_repository.dart';

class DermatologistList extends StatefulWidget {
  final List<double> userLocation;
  final Diagnosis? diagnosis;

  DermatologistList({
    required this.userLocation, this.diagnosis,
  });

  @override
  _DermatologistListState createState() =>
      _DermatologistListState();
}

class _DermatologistListState extends State<DermatologistList> {
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

  void _viewDetails(Dermatologist dermatologist) {
    // Code to show dermatologist details
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
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
          onTap: () => _viewDetails(dermatologist),
        );
      },
    );
  }
}
