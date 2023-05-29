import 'package:flutter/material.dart';

import 'appointments_list.dart';


class AppointmentsPage extends StatelessWidget {
  final bool completed;

  AppointmentsPage({Key? key, required this.completed}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('${completed ? "Completed" : "Scheduled"} Appointments'),
      ),
      body: AppointmentList(completed: completed),
    );
  }
}