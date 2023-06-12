import 'dermatologist.dart';

class Slot {
  DateTime startTime;
  int dermatologistId;
  bool scheduled;
  int dayOfWeek;

  Slot({
    required this.startTime,
    required this.dermatologistId,
    this.scheduled = false,
    required this.dayOfWeek,
  });

  factory Slot.fromJson(Map<String, dynamic> json) {
    return Slot(
      startTime: DateTime.parse(json['start_time']),
      dermatologistId: json['dermatologist'],
      scheduled: json['scheduled'],
      dayOfWeek: json['day_of_week'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'start_time': startTime.toIso8601String(),
      'dermatologist_id': dermatologistId,
      'scheduled': scheduled,
      'day_of_week': dayOfWeek,
    };
  }
}