
import 'treatment.dart';

class Disease {
  final String name;
  final String description;
  final String severity;
  final List<Treatment> treatments;

  Disease({required this.name, required this.description, required this.severity, required this.treatments});

  factory Disease.fromJson(Map<String, dynamic> json) {
    return Disease(
      name: json['name'],
      description: json['description'],
      severity: json['severity'],
      treatments: json['treatments'].map((e) => Treatment.fromJson(e)).toList().cast<Treatment>(),
    );
  }
}