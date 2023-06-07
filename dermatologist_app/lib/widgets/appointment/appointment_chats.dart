import 'package:dermatologist_app/main.dart';
import 'package:flutter/material.dart';
import 'package:dermatologist_app/models/appointment_chat.dart';
import 'package:dermatologist_app/repositories/appointment_repository.dart';
import 'appointment_chat_page.dart';

class AppointmentChats extends StatefulWidget {
  AppointmentChats({Key? key}) : super(key: key);

  @override
  AppointmentChatsState createState() => AppointmentChatsState();
}


class AppointmentChatsState extends State<AppointmentChats> {
  final AppointmentRepository appointmentChatRepository =
      AppointmentRepository();
  Future<List<AppointmentChat>> _chatsFuture = Future.value([]);

  void _loadChats() {
    setState(() {
      _chatsFuture = appointmentChatRepository.getAppointmentChats();
    });
  }

  @override
  void initState() {
    super.initState();
    _loadChats();
  }
  @override
  Widget build(BuildContext context) {

    return Scaffold(
      //appBar: AppBar(title: const Text('Appointment Chats')),
      body: FutureBuilder<List<AppointmentChat>>(
        future: _chatsFuture,
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
                  leading: const CircleAvatar(
                    backgroundColor: Colors.grey,
                    child: Icon(Icons.person),
                  ),
                  title: Text('${chat.patient.user?.firstName} ${chat.patient.user?.lastName}'),
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
                    Navigator.of(context).push(MaterialPageRoute(
                        builder: (context) => AppointmentChatPage(chat: chat)));
                  },
                );
              },
            );
          } else if (snapshot.hasError) {
            return Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('Error: ${snapshot.error}'),
                SizedBox(height: 16),
                ElevatedButton(
                  onPressed: _loadChats,
                  child: Text('Retry'),
                ),
              ],
            );
          } else {
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
    );
  }
}
