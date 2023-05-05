
class Prediction {
  late int disease;
  late double probability;
  late int diagnosis;

  Prediction({required this.disease, required this.probability, required this.diagnosis});

  factory Prediction.fromJson(Map<String, dynamic> json) {
    return Prediction(
      disease: json['disease'],
      probability: json['probability'],
      diagnosis: json['diagnosis'],
    );
  }

  Map<String, dynamic> toJson() => {
    'disease': disease,
    'probability': probability,
    'diagnosis': diagnosis,
  };
}