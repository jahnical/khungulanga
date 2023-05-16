import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:intl/intl.dart';
import 'package:khungulanga_app/models/chat_message.dart';
import 'package:khungulanga_app/repositories/appointment_chat_repository.dart';
import 'package:khungulanga_app/widgets/common/common.dart';

import '../../blocs/appointment_bloc/appointment_chat_bloc.dart';
import '../../models/dermatologist.dart';
import '../../models/diagnosis.dart';


class AppointmentChatPage extends StatefulWidget {
  final Dermatologist dermatologist;
  Diagnosis? diagnosis;

  AppointmentChatPage({
    required this.dermatologist,
    this.diagnosis,
  });

  @override
  _AppointmentChatPageState createState() => _AppointmentChatPageState();
}

class _AppointmentChatPageState extends State<AppointmentChatPage> {
  //late Appointment _appointment;
  late TextEditingController _messageController;
  //List<ChatMessage> _messages = [];

  @override
  void initState() {
    super.initState();
    _messageController = TextEditingController();
  }

  void _sendMessage(AppointmentChatBloc bloc) {
    if (_messageController.text.trim().isEmpty) return;

    final newMessage = ChatMessage(
      sender: bloc.chat!.patient.user!,
      text: _messageController.text.trim(),
      chat: bloc.chat!,
      time: DateTime.now(),
      seen: false,
    );

    final data = FormData.fromMap(newMessage.toJsonMap());

    bloc.add(SendMessage(data));
  }

  bool _isExpanded = false;
  Widget _buildAppointmentCard(AppointmentChatBloc appointmentChatBloc) {
    return Card(
      margin: EdgeInsets.symmetric(horizontal: 0.0, vertical: 0.0),
      child: Padding(
        padding: EdgeInsets.all(8.0),
        child: appointmentChatBloc.state is UpdatingAppointment? LoadingIndicator() : Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            InkWell(
              onTap: () {
                setState(() {
                  _isExpanded = !_isExpanded;
                });
              },
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Appointment Details',
                    style: Theme.of(context).textTheme.headline6,
                  ),
                  Icon(
                    _isExpanded ? Icons.expand_less : Icons.expand_more,
                  ),
                ],
              ),
            ),
            if (_isExpanded)
              Column(
                children: [
                  SizedBox(height: 8.0),
                  TextFormField(
                    initialValue:
                    '${appointmentChatBloc.chat!.appointment.dermatologist.user.firstName} ${appointmentChatBloc.chat!.appointment.dermatologist.user.lastName}',
                    decoration: InputDecoration(labelText: 'Dermatologist'),
                    enabled: false,
                  ),
                  TextFormField(
                    initialValue:
                    DateFormat('dd/MM/yyyy hh:mm').format(appointmentChatBloc.chat!.appointment.appoDate ?? DateTime.now()),
                    decoration: InputDecoration(labelText: 'Time'),
                    onChanged: (value) {
                      // Update the appointment object with the new time value
                      // _appointment.appoTime = value;
                    },
                  ),
                  TextFormField(
                    initialValue:
                    appointmentChatBloc.chat!.appointment.duration?.inHours.toString(),
                    decoration: InputDecoration(labelText: 'Duration (hours)'),
                    onChanged: (value) {
                      // Update the appointment object with the new duration value
                      // _appointment.duration = value;
                    },
                  ),
                  TextFormField(
                    initialValue: appointmentChatBloc.chat!.appointment.cost.toString(),
                    decoration: InputDecoration(labelText: 'Cost'),
                    onChanged: (value) {
                      // Update the appointment object with the new cost value
                      // _appointment.cost = value;
                    },
                  ),
                  SizedBox(height: 16.0),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      ElevatedButton(
                        onPressed: () {
                          // Save the updated appointment
                          // _onAppointmentChange(_appointment.copyWith(patient_approved: true));
                        },
                        child: Text('Approve'),
                      ),
                      SizedBox(width: 16.0),
                      ElevatedButton(
                        onPressed: () {
                          // Save the updated appointment
                          // _onAppointmentChange(_appointment.copyWith(patient_approved: false));
                        },
                        child: Text('Reject'),
                      ),
                    ],
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildMessageList(AppointmentChatBloc appointmentChatBloc) {
    return ListView.builder(
      itemCount: appointmentChatBloc.chat!.messages.length,
      itemBuilder: (context, index) {
        final message = appointmentChatBloc.chat!.messages[index];
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

  Widget _buildMessageInput(AppointmentChatBloc appointmentChatBloc) {
    return Padding(
      padding: EdgeInsets.all(8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Expanded(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: TextField(
                controller: _messageController,
                decoration: InputDecoration(
                  hintText: 'Type your message',
                  filled: true,
                  fillColor: Colors.grey.shade200,
                  contentPadding: EdgeInsets.symmetric(vertical: 12.0, horizontal: 16.0),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(25.0),
                    borderSide: BorderSide.none,
                  ),
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: ElevatedButton(
              onPressed: () => {_sendMessage(appointmentChatBloc)},
              child: appointmentChatBloc.state is AppointmentChatMessageSending? const LoadingIndicator() : const Icon(Icons.send),
            ),
          )
        ],
      ),
    );
  }
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<AppointmentChatBloc, AppointmentChatState>(
      bloc: AppointmentChatBloc(RepositoryProvider.of<AppointmentChatRepository>(context)),
      builder: (context, state) {
        if (state is AppointmentChatInitial || state is AppointmentChatLoading) {
          return const Center(
            child: CircularProgressIndicator(),
          );
        } else {
          return Scaffold(
            appBar: AppBar(
              title: Text('${BlocProvider.of<AppointmentChatBloc>(context).chat!.dermatologist.user.firstName} ${BlocProvider.of<AppointmentChatBloc>(context).chat!.dermatologist.user.lastName}'),
            ),
            body: Column(
              children: [
                _buildAppointmentCard(BlocProvider.of<AppointmentChatBloc>(context)),
                Expanded(
                  child: _buildMessageList(BlocProvider.of<AppointmentChatBloc>(context)),
                ),
                _buildMessageInput(BlocProvider.of<AppointmentChatBloc>(context)),
              ],
            ),
          );
        }
      },
    );
  }
}