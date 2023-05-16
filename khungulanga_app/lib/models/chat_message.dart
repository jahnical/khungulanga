import 'appointment_chat.dart';
import 'diagnosis.dart';
import 'appointment.dart';
import 'user.dart';

class ChatMessage {
  final int? id;
  final User sender;
  final String text;
  final AppointmentChat chat;
  final Diagnosis? diagnosis;
  final Appointment? appointment;
  final DateTime time;
  final bool seen;

  ChatMessage({
    this.id,
    required this.sender,
    required this.text,
    required this.chat,
    this.diagnosis,
    this.appointment,
    required this.time,
    required this.seen,
  });

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      id: json['id'],
      sender: User.fromJson(json['sender']),
      text: json['text'],
      chat: AppointmentChat.fromJson(json['chat']),
      diagnosis: json['diagnosis'] != null ? Diagnosis.fromJson(json['diagnosis']) : null,
      appointment: json['appointment'] != null ? Appointment.fromJson(json['appointment']) : null,
      time: DateTime.parse(json['time']),
      seen: json['seen'],
    );
  }

  Map<String, dynamic> toJsonMap() {
    return {
      'id': id,
      'sender': sender.toJson(),
      'text': text,
      'chat': chat.id,
      'diagnosis': diagnosis?.id,
      'appointment': appointment?.id,
      'time': time.toIso8601String(),
      'seen': seen,
    };
  }
}