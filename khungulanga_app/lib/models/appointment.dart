import 'dart:developer';

import 'package:flutter/foundation.dart';

import 'dermatologist.dart';
import 'patient.dart';

class Appointment {
  final int? id;
  final Dermatologist dermatologist;
  final Patient? patient;
  DateTime? bookDate;
  DateTime? appoDate;
  bool done;
  Duration? duration;
  double? cost;
  DateTime? patientApproved;
  DateTime? dermatologistApproved;
  DateTime? patientRejected;
  DateTime? dermatologistRejected;
  String extraInfo;

  Appointment({
    this.id,
    required this.dermatologist,
    this.patient,
    this.bookDate,
    this.appoDate,
    this.done = false,
    this.duration = const Duration(hours: 1),
    this.cost = 0.0,
    this.patientApproved,
    this.dermatologistApproved,
    this.patientRejected,
    this.dermatologistRejected,
    this.extraInfo = "",
  });

  factory Appointment.fromJson(Map<String, dynamic> json) {
    return Appointment(
      id: json['id'],
      dermatologist: Dermatologist.fromJson(json['dermatologist']),
      patient: json['patient'] != null ? Patient.fromJson(json['patient']) : null,
      bookDate: json['book_date'] != null ? DateTime.parse(json['book_date']) : null,
      appoDate: json['appo_date'] != null ? DateTime.parse(json['appo_date']) : null,
      done: json['done'] ?? false,
      duration: json['duration'] != null ? Duration(minutes: json['duration'] ?? 0) : null,
      cost: json['cost']?.toDouble() ?? 0.0,
      patientApproved: json['patient_approved'] != null ? DateTime.parse(json['patient_approved']) : null,
      dermatologistApproved: json['dermatologist_approved'] != null ? DateTime.parse(json['dermatologist_approved']) : null,
      patientRejected: json['patient_rejected'] != null ? DateTime.parse(json['patient_rejected']) : null,
      dermatologistRejected: json['dermatologist_rejected'] != null ? DateTime.parse(json['dermatologist_rejected']) : null,
      extraInfo: json['extra_info'] ?? "",
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
      'duration': duration?.inMinutes,
      'cost': cost,
      'extra_info': extraInfo,
      'patient_approved': patientApproved?.toIso8601String(),
      'dermatologist_approved': dermatologistApproved?.toIso8601String(),
      'patient_rejected': patientRejected?.toIso8601String(),
      'dermatologist_rejected': dermatologistRejected?.toIso8601String(),
    };
  }

  Appointment copyWith({
    int? id,
    Dermatologist? dermatologist,
    Patient? patient,
    DateTime? bookDate,
    DateTime? appoDate,
    bool? done,
    Duration? duration,
    double? cost,
    DateTime? patientApproved,
    DateTime? dermatologistApproved,
    DateTime? patientRejected,
    DateTime? dermatologistRejected,
    String? extraInfo,
  }) {
    return Appointment(
      id: id ?? this.id,
      dermatologist: dermatologist ?? this.dermatologist,
      patient: patient ?? this.patient,
      bookDate: bookDate ?? this.bookDate,
      appoDate: appoDate ?? this.appoDate,
      done: done ?? this.done,
      duration: duration ?? this.duration,
      cost: cost ?? this.cost,
      patientApproved: patientApproved ?? this.patientApproved,
      dermatologistApproved: dermatologistApproved ?? this.dermatologistApproved,
      patientRejected: patientRejected ?? this.patientRejected,
      dermatologistRejected: dermatologistRejected ?? this.dermatologistRejected,
      extraInfo: extraInfo ?? this.extraInfo,
    );
  }
}
