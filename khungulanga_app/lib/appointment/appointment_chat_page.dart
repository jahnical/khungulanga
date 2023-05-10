import 'package:flutter/material.dart';

// Replace these with the appropriate models for your project
import '../models/appointment_chat.dart';
import '../models/chat_message.dart';
import '../models/dermatologist.dart';
import '../models/diagnosis.dart';
import '../models/appointment.dart';
import '../models/patient.dart';


class AppointmentChatPage extends StatefulWidget {
  final Dermatologist dermatologist;
  final Patient? patient = null;
  Diagnosis? diagnosis;

  AppointmentChatPage({
    required this.dermatologist,
    this.diagnosis,
  });

  @override
  _AppointmentChatPageState createState() => _AppointmentChatPageState();
}

class _AppointmentChatPageState extends State<AppointmentChatPage> {
  late Appointment _appointment;
  late TextEditingController _messageController;
  List<ChatMessage> _messages = [];

  @override
  void initState() {
    super.initState();
    _appointment = Appointment(
      dermatologist: widget.dermatologist,
      patient: widget.patient,
      bookDate: DateTime.now(),
      appoDate: DateTime.now().add(Duration(days: 7)),
      duration: Duration(hours: 1),
      cost: 100.0,
      patientApproved: false,
      dermatologistApproved: false,
    );
    _messageController = TextEditingController();
  }

  void _onAppointmentChange(Appointment newAppointment) {
    setState(() {
      _appointment = newAppointment;
    });
  }

  void _sendMessage() {
    if (_messageController.text.trim().isEmpty) return;

    final newMessage = ChatMessage(
      sender: widget.patient!.user!,
      text: _messageController.text.trim(),
      chat: AppointmentChat(
        patient: widget.patient!,
        diagnosis: null,
        dermatologist: widget.dermatologist,
        appointment: _appointment,
      ),
      date: DateTime.now(),
      time: DateTime.now(),
      seen: false,
    );

    setState(() {
      _messages.add(newMessage);
      _messageController.clear();
    });
  }

  Widget _buildAppointmentCard() {
    return Card(
      margin: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
      child: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'Appointment Details',
              style: Theme.of(context).textTheme.headline6,
            ),
            SizedBox(height: 16.0),
            Text('Dermatologist: ${_appointment.dermatologist.user.firstName} ${_appointment.dermatologist.user.lastName}'),
            Text('Date: ${_appointment.appoDate.toString()}'),
            Text('Time: ${_appointment.appoDate.toString()}'),
            Text('Duration: ${_appointment.duration.inHours} hours'),
            Text('Cost: ${_appointment.cost}'),
            SizedBox(height: 16.0),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: null,//() => _onAppointmentChange(_appointment.copyWith(patient_approved: true)),
                  child: Text('Approve'),
                ),
                SizedBox(width: 16.0),
                ElevatedButton(
                  onPressed: null,//() => _onAppointmentChange(_appointment.copyWith(patient_approved: false)),
                  child: Text('Reject'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMessageList() {
    return ListView.builder(
      itemCount: _messages.length,
      itemBuilder: (context, index) {
        final message = _messages[index];
        return ListTile(
          title: Text(message.sender.firstName),
          subtitle: Text(message.text),
          trailing: Icon(
            message.seen ? Icons.check_circle : Icons.check_circle_outline,
            color: message.seen ? Colors.green : Colors.grey,
          ),
        );
      },
    );
  }

  Widget _buildMessageInput() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: TextField(
              controller: _messageController,
              decoration: InputDecoration(
                hintText: 'Type your message',
              ),
            ),
          ),
        ),
        ElevatedButton(
          onPressed: _sendMessage,
          child: Text('Send'),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Appointment Chat'),
      ),
      body: Material(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _buildAppointmentCard(),
            Expanded(
              child: _buildMessageList(),
            ),
            _buildMessageInput(),
          ],
        ),
      ),
    );
  }
}
