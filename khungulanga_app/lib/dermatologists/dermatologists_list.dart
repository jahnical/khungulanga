import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:khungulanga_app/appointment/appointment_chat_page.dart';
import 'package:khungulanga_app/models/dermatologist.dart';
import 'package:khungulanga_app/models/diagnosis.dart';
import 'package:khungulanga_app/repositories/dermatologist_repository.dart';

class DermatologistList extends StatefulWidget {
  final List<double> userLocation;
  final Diagnosis? diagnosis;

  DermatologistList({
    required this.userLocation,
    this.diagnosis,
  });

  @override
  _DermatologistListState createState() => _DermatologistListState();
}

class _DermatologistListState extends State<DermatologistList> {
  List<Dermatologist> dermatologists = [];
  bool isLoading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    _loadDermatologists();
  }

  void _loadDermatologists() async {
    try {
      dermatologists = await DermatologistRepository().getNearbyDermatologists(
          widget.userLocation[0], widget.userLocation[1]);
      setState(() {
        isLoading = false;
        error = null;
      });
    } catch (e) {
      log('Failed to load dermatologists: $e');
      setState(() {
        isLoading = false;
        error = 'Failed to load dermatologists';
      });
    }
  }

  void _bookAppointment(Dermatologist dermatologist) {
    // Code to navigate to appointment chat screen
    Navigator.push(context, MaterialPageRoute(builder: (_) {
      return AppointmentChatPage(
        dermatologist: dermatologist,
        diagnosis: widget.diagnosis,
      );
    }));
  }

  void _viewDetails(Dermatologist dermatologist) {
    // Code to show dermatologist details
  }

  Widget _buildLoadingIndicator() {
    return Center(
      child: CircularProgressIndicator(),
    );
  }

  Widget _buildError() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(error!),
          SizedBox(height: 16.0),
          ElevatedButton(
            onPressed: _retryLoadDermatologists,
            child: Text('Retry'),
          ),
        ],
      ),
    );
  }

  void _retryLoadDermatologists() {
    setState(() {
      isLoading = true;
      error = null;
    });
    _loadDermatologists();
  }


  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return _buildLoadingIndicator();
    }

    if (error != null) {
      return _buildError();
    }

    return ListView.builder(
      itemCount: dermatologists.length,
      itemBuilder: (BuildContext context, int index) {
        final dermatologist = dermatologists[index];
        return Column(
          children: [
            SizedBox(height: 8.0),
            ListTile(
              leading: const Icon(Icons.person_outline),
              title: Text(
                '${dermatologist.user.firstName} ${dermatologist.user.lastName}',
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 16.0,
                ),
              ),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SizedBox(height: 4.0),
                  Text(dermatologist.qualification),
                  SizedBox(height: 4.0),
                  Text(dermatologist.clinic),
                ],
              ),
              trailing: IconButton(
                icon: Icon(Icons.book, color: Theme.of(context).primaryColor),
                onPressed: () => _bookAppointment(dermatologist),
              ),
              onTap: () => _viewDetails(dermatologist),
            ),
            SizedBox(height: 8.0),
            Divider(height: 1.0, thickness: 1.0),
          ],
        );
      },
    );
  }
}