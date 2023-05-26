import 'package:flutter/material.dart';
import 'package:dermatologist_app/models/appointment.dart';

class AppointmentDetailPage extends StatelessWidget {
  final Appointment appointment;

  AppointmentDetailPage({required this.appointment});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.blue[50],
      appBar: AppBar(
        title: Text('Appointment Details'),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(height: 16.0),
            AppointmentDetailCard(
              title: 'Dermatologist',
              icon: Icons.person,
              content:
                  '${appointment.dermatologist.user.firstName} ${appointment.dermatologist.user.lastName}',
            ),
            SizedBox(height: 16.0),
            AppointmentDetailCard(
              title: 'Patient',
              icon: Icons.person,
              content:
                  '${appointment.patient?.user?.firstName} ${appointment.patient?.user?.lastName}',
            ),
            SizedBox(height: 16.0),
            AppointmentDetailCard(
              title: 'Appointment Date',
              icon: Icons.calendar_today,
              content: '${appointment.appoTime ?? 'N/A'}',
            ),
            SizedBox(height: 16.0),
            AppointmentStatusCard(
              appointment: appointment,
            ),
            SizedBox(height: 16.0),
            AppointmentDetailCard(
              title: 'Duration',
              icon: Icons.timer,
              content: '${appointment.duration?.inHours ?? 0} hours',
            ),
            SizedBox(height: 16.0),
            AppointmentDetailCard(
              title: 'Cost',
              icon: Icons.money,
              content: '\$${appointment.cost ?? 0.0}',
            ),
            SizedBox(height: 16.0),
            AppointmentDetailCard(
              title: 'Extra Information',
              icon: Icons.info,
              content: '${appointment.extraInfo}',
            ),
          ],
        ),
      ),
    );
  }
}

class AppointmentDetailCard extends StatelessWidget {
  final String title;
  final IconData? icon;
  final String content;

  AppointmentDetailCard({
    required this.title,
    this.icon,
    required this.content,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      //color: Colors.blue[50],
      elevation: 4.0,
      child: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 8.0),
            if (icon != null)
              Row(
                children: [
                  Icon(icon, size: 24),
                  SizedBox(width: 8.0),
                  Text(
                    content,
                    style: TextStyle(fontSize: 16),
                  ),
                ],
              ),
            if (icon == null)
              Text(
                content,
                style: TextStyle(fontSize: 16),
              ),
          ],
        ),
      ),
    );
  }
}

class AppointmentStatusCard extends StatelessWidget {
  final Appointment appointment;

  AppointmentStatusCard({required this.appointment});

  @override
  Widget build(BuildContext context) {
    return Card(
      //color: Colors.blue[50],
      elevation: 4.0,
      child: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Status',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 8.0),
            Row(
              children: [
                Icon(
                  appointment.done ? Icons.check_circle : Icons.schedule,
                  color: appointment.done ? Colors.green : Colors.orange,
                  size: 24,
                ),
                SizedBox(width: 8.0),
                Text(
                  appointment.done ? 'Completed' : 'Scheduled',
                  style: TextStyle(fontSize: 16),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
