
import 'prediction.dart';

class Diagnosis {
  final String imageUrl;
  final String bodyPart;
  final bool itchy;
  final DateTime date;
  final List<Prediction> predictions;

  Diagnosis({required this.imageUrl, required this.bodyPart, required this.itchy, required this.date, required this.predictions});

  factory Diagnosis.fromJson(Map<String, dynamic> json) {
    return Diagnosis(
      imageUrl: json['image'],
      bodyPart: json['body_part'],
      itchy: json['itchy'],
      date: DateTime.parse(json['date']),
      predictions: json['predictions'].map((e) => Prediction.fromJson(e)).toList().cast<Prediction>(),
    );
  }
}