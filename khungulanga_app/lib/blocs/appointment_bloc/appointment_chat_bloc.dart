import 'dart:async';
import 'dart:developer';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:khungulanga_app/models/appointment.dart';
import 'package:khungulanga_app/repositories/appointment_chat_repository.dart';
import 'package:khungulanga_app/repositories/user_repository.dart';
import 'package:meta/meta.dart';

import '../../models/appointment_chat.dart';
import '../../models/chat_message.dart';
import '../../models/dermatologist.dart';
import '../../models/patient.dart';

part 'appointment_chat_event.dart';
part 'appointment_chat_state.dart';

class AppointmentChatBloc extends Bloc<AppointmentChatEvent, AppointmentChatState> {
  final AppointmentChatRepository _appointmentChatRepository;
  final UserRepository _userRepository;

  AppointmentChat? chat;

  AppointmentChatBloc(this._appointmentChatRepository, this._userRepository) : super(AppointmentChatInitial()) {}

  Future<AppointmentChat> _createAppointmentChat(FetchAppointmentChat event) async {
    final patient = await _userRepository.fetchPatient(USER!.username);
    return AppointmentChat(
      patient: patient,
      diagnosis: null,
      dermatologist: event.dermatologist!,
      messages: [],
      appointment: Appointment(
        dermatologist: event.dermatologist!,
        patient: patient,
      ),
    );
  }

  @override
  Stream<AppointmentChatState> mapEventToState(
    AppointmentChatEvent event,
  ) async* {
    log(event.toString());
    if (event is FetchAppointmentChat) {
      if (event.appointmentChatId == null) {
        final chat = await _createAppointmentChat(event);
        this.chat = await _appointmentChatRepository.saveAppointmentChat(chat);
        yield AppointmentChatLoaded(chat);
      } else {
        yield AppointmentChatLoading();
        try {
          final chat = await _appointmentChatRepository.getAppointmentChat(event.appointmentChatId!);
          this.chat = chat;
          yield AppointmentChatLoaded(chat);
        } on DioError catch (e) {
          yield AppointmentChatError(message: e.response!.data['message']);
        }
      }
    }

    else if (event is SendMessage) {
      yield AppointmentChatMessageSending();
      try {
        final message = await _appointmentChatRepository.sendMessage(event.data);
        chat!.messages.add(message);
        yield AppointmentChatLoaded(chat!);
      } on DioError catch (e) {
        yield AppointmentChatError(message: e.response?.toString() ?? "Error Sending Message");
      }
    }

    else if (event is ApproveAppointment) {
      yield UpdatingAppointment();
      try {
        chat!.appointment.patientApproved = DateTime.now();
        await _appointmentChatRepository.updateAppointment(chat!.appointment);
        yield AppointmentUpdated(chat!);
      } on DioError catch (e) {
        yield AppointmentChatError(message: e.response!.data['message']);
      }
    }

    else if (event is RejectAppointment) {
      yield UpdatingAppointment();
      try {
        chat!.appointment.patientRejected = DateTime.now();
        await _appointmentChatRepository.updateAppointment(chat!.appointment);
        yield AppointmentUpdated(chat!);
      } on DioError catch (e) {
        yield AppointmentChatError(message: e.response!.data['message']);
      }
    }

    else if (event is FetchAppointmentChatMessages) {
      yield AppointmentChatLoading();
      try {
        final messages = await _appointmentChatRepository.getAppointmentChatMessages(event.appointmentChatId);
        chat!.messages = messages;
        yield AppointmentChatLoaded(chat!);
      } on DioError catch (e) {
        yield AppointmentChatError(message: e.response!.data['message']);
      }
    }
  }
}
