part of 'appointment_chat_bloc.dart';

@immutable
abstract class AppointmentChatEvent {}

class FetchAppointmentChat extends AppointmentChatEvent {
  final int? appointmentChatId;
  final Dermatologist? dermatologist;
  final Patient? patient;
  final BuildContext? context;
  FetchAppointmentChat(this.appointmentChatId, this.dermatologist, this.patient, this.context);
}

class SendMessage extends AppointmentChatEvent {
  final FormData data;

  SendMessage(this.data);
}

class ApproveAppointment extends AppointmentChatEvent {
  final int appointmentChatId;

  ApproveAppointment(this.appointmentChatId);
}

class RejectAppointment extends AppointmentChatEvent {
  final int appointmentChatId;

  RejectAppointment(this.appointmentChatId);
}

class CancelAppointment extends AppointmentChatEvent {
  final int appointmentChatId;

  CancelAppointment(this.appointmentChatId);
}

class CompleteAppointment extends AppointmentChatEvent {
  final int appointmentChatId;

  CompleteAppointment(this.appointmentChatId);
}

class FetchAppointmentChatMessages extends AppointmentChatEvent {
  final int appointmentChatId;

  FetchAppointmentChatMessages(this.appointmentChatId);
}

class FetchAppointmentChats extends AppointmentChatEvent {}

