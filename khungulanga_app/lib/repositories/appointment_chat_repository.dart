import 'package:dio/dio.dart';
import 'package:khungulanga_app/models/appointment.dart';
import 'package:khungulanga_app/models/chat_message.dart';
import '../api_connection/con_options.dart';
import '../api_connection/endpoints.dart';
import '../models/appointment_chat.dart';


class AppointmentChatRepository {
  final Dio _dio = Dio();
  // This could be replaced with an API call or database query
  Future<List<AppointmentChat>> getAppointmentChats() async {
    return await [

    ];
  }

  Future<AppointmentChat> getAppointmentChat(int id) async {
    final response = await _dio.get('$APPOINTMENT_CHAT_URL/$id/', options: getOptions());
    final chatJson = response.data as Map<String, dynamic>;
    final chat = AppointmentChat.fromJson(chatJson);
    return chat;
  }

  Future<AppointmentChat> saveAppointmentChat(AppointmentChat chat) async {
    final response = await _dio.post('$APPOINTMENT_CHAT_URL/', options: postOptions(), data: chat.toJsonMap());

    if (response.statusCode != 201) {
      throw Exception('Failed to create appointment chat');
    } else {
      final chatJson = response.data as Map<String, dynamic>;
      final createdChat = AppointmentChat.fromJson(chatJson);
      return createdChat;
    }
  }

  Future<ChatMessage> sendMessage(FormData data) async {
    final response = await _dio.post('$APPOINTMENT_CHAT_URL/send_message/', options: postOptions(), data: data);

    if (response.statusCode != 201) {
      throw Exception('Failed to send message');
    } else {
      final messageJson = response.data as Map<String, dynamic>;
      final message = ChatMessage.fromJson(messageJson);
      return message;
    }
  }

  Future<List<ChatMessage>> getAppointmentChatMessages(int appointmentChatId) async {
    final response = await _dio.get('$APPOINTMENT_CHAT_URL/$appointmentChatId/messages/', options: getOptions());

    if (response.statusCode != 200) {
      throw Exception('Failed to get appointment chat messages');
    } else {
      final messagesJson = response.data as List<dynamic>;
      final messages = messagesJson.map((messageJson) => ChatMessage.fromJson(messageJson)).toList();
      return messages;
    }
  }

  Future<Appointment> updateAppointment(Appointment appointment) async {
    final response = await _dio.patch('$APPOINTMENTS_URL/${appointment.id}/', options: patchOptions(), data: appointment.toJson());

    if (response.statusCode != 200) {
      throw Exception('Failed to update appointment');
    } else {
      final appointmentJson = response.data as Map<String, dynamic>;
      final updatedAppointment = Appointment.fromJson(appointmentJson);
      return updatedAppointment;
    }
  }
}