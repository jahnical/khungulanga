import 'package:flutter/foundation.dart';

import 'dermatologist.dart';
import 'patient.dart';

class Appointment {
  final int? id;
  final Dermatologist dermatologist;
  final Patient? patient;
  final DateTime bookDate;
  final DateTime appoDate;
  bool done = false;
  final Duration duration;
  final double cost;
  final bool patientApproved;
  final bool dermatologistApproved;

  Appointment({
    this.id,
    this.done = false,
    required this.dermatologist,
    required this.patient,
    required this.bookDate,
    required this.appoDate,
    required this.duration,
    required this.cost,
    required this.patientApproved,
    required this.dermatologistApproved,
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

  /*Map<String, dynamic> toJson() {
    return {
      'id': id,
      'dermatologist': dermatologist.toJson(),
      'patient': patient.toJson(),
      'book_date': bookDate.toIso8601String(),
      'appo_date': appoDate.toIso8601String(),
      'done': done,
      'duration': duration.inMilliseconds,
      'cost': cost,
      'patient_approved': patientApproved,
      'dermatologist_approved': dermatologistApproved,
    };
  }*/
}
