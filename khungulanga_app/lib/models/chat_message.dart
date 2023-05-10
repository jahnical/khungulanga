import 'appointment_chat.dart';
import 'diagnosis.dart';
import 'appointment.dart';
import 'user.dart';

class ChatMessage {
  final User sender;
  final String text;
  final AppointmentChat chat;
  final Diagnosis? diagnosis;
  final Appointment? appointment;
  final DateTime date;
  final DateTime time;
  final bool seen;

  ChatMessage({
    required this.sender,
    required this.text,
    required this.chat,
    this.diagnosis,
    this.appointment,
    required this.date,
    required this.time,
    required this.seen,
  });

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      sender: User.fromJson(json['sender']),
      text: json['text'],
      chat: AppointmentChat.fromJson(json['chat']),
      diagnosis: json['diagnosis'] != null ? Diagnosis.fromJson(json['diagnosis']) : null,
      appointment: json['appointment'] != null ? Appointment.fromJson(json['appointment']) : null,
      date: DateTime.parse(json['date']),
      time: DateTime.parse(json['time']),
      seen: json['seen'],
    );
  }
}