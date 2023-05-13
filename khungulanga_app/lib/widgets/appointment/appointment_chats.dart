import 'package:flutter/material.dart';
import 'package:khungulanga_app/models/appointment_chat.dart';
import 'package:khungulanga_app/repositories/appointment_chat_repository.dart';


class AppointmentChatsList extends StatelessWidget {
  final AppointmentChatRepository appointmentChatRepository =
  AppointmentChatRepository();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Appointment Chats')),
      body: FutureBuilder<List<AppointmentChat>>(
        future: appointmentChatRepository.getAppointmentChats(),
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            final appointmentChats = snapshot.data!;

            return ListView.builder(
              itemCount: appointmentChats.length,
              itemBuilder: (context, index) {
                final chat = appointmentChats[index];
                final lastMessage = chat.messages.isNotEmpty
                    ? chat.messages.last.text
                    : 'No messages yet';

                return ListTile(
                  leading: CircleAvatar(
                    child: Icon(Icons.person),
                    backgroundColor: Colors.grey,
                  ),
                  title: Text(chat.dermatologist.user.firstName),
                  subtitle: Text(lastMessage),
                  trailing: chat.messages.isNotEmpty
                      ? Icon(
                    chat.messages.last.seen
                        ? Icons.check_circle
                        : Icons.check_circle_outline,
                    color: chat.messages.last.seen
                        ? Colors.green
                        : Colors.grey,
                  )
                      : null,
                  onTap: () {
                    // Navigate to the appointment chat page
                  },
                );
              },
            );
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else {
            return Center(child: CircularProgressIndicator());
          }
        },
      ),
    );
  }
}
