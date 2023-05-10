import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import 'appointment.dart';
import 'dermatologist.dart';
import 'diagnosis.dart';
import 'patient.dart';

class AppointmentChat {
  final Patient patient;
  final Diagnosis? diagnosis;
  final Dermatologist dermatologist;
  final Appointment appointment;

  AppointmentChat({
    required this.patient,
    required this.diagnosis,
    required this.dermatologist,
    required this.appointment,
  });

  factory AppointmentChat.fromJson(Map<String, dynamic> json) {
    return AppointmentChat(
      patient: Patient.fromJson(json['patient']),
      diagnosis: Diagnosis.fromJson(json['diagnosis']),
      dermatologist: Dermatologist.fromJson(json['dermatologist']),
      appointment: Appointment.fromJson(json['appointment']),
    );
  }

  /*Map<String, dynamic> toJson() {
    return {
      'patient': patient.toJson(),
      'diagnosis': diagnosis.toJson(),
      'dermatologist': dermatologist.toJson(),
      'appointment': appointment.toJson(),
    };
  }*/
}