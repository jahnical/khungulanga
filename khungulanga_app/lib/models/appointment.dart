import 'package:flutter/foundation.dart';

import 'dermatologist.dart';
import 'patient.dart';

class Appointment {
  final int? id;
  final Dermatologist dermatologist;
  final Patient? patient;
  DateTime? bookDate;
  DateTime? appoDate;
  bool done = false;
  Duration? duration = const Duration(hours: 1);
  double? cost = 0.0;
  DateTime? patientApproved;
  DateTime? dermatologistApproved;
  DateTime? patientRejected;
  DateTime? dermatologistRejected;


  Appointment({
    this.id,
    this.done = false,
    required this.dermatologist,
    required this.patient,
    this.bookDate,
    this.appoDate,
    this.duration,
    this.cost,
    this.patientApproved,
    this.dermatologistApproved,
    this.patientRejected,
    this.dermatologistRejected,
  });

  factory Appointment.fromJson(Map<String, dynamic> json) {
    return Appointment(
      id: json['id'],
      dermatologist: Dermatologist.fromJson(json['dermatologist']),
      patient: Patient.fromJson(json['patient']),
      bookDate: DateTime.parse(json['book_date']),
      appoDate: DateTime.parse(json['appo_date']),
      done: json['done'],
      duration: Duration(milliseconds: json['duration']),
      cost: json['cost'].toDouble(),
      patientApproved: json['patient_approved'],
      dermatologistApproved: json['dermatologist_approved'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'dermatologist_id': dermatologist.id,
      'patient_id': patient?.id,
      'book_date': bookDate?.toIso8601String(),
      'appo_date': appoDate?.toIso8601String(),
      'done': done,
      'duration': duration?.inMilliseconds,
      'cost': cost,
      'patient_approved': patientApproved,
      'dermatologist_approved': dermatologistApproved,
      'patient_rejected': patientRejected,
      'dermatologist_rejected': dermatologistRejected,
    };
  }
}