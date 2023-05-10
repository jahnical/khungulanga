import 'user.dart';

class Dermatologist {
  int id;
  String qualification;
  String workEmail;
  String phoneNumber1;
  String phoneNumber2;
  String clinic;
  double locationLat;
  double locationLon;
  String locationDesc;
  User user;

  Dermatologist({
    required this.id,
    required this.qualification,
    required this.workEmail,
    required this.phoneNumber1,
    required this.phoneNumber2,
    required this.clinic,
    required this.locationLat,
    required this.locationLon,
    required this.locationDesc,
    required this.user,
  });

  factory Dermatologist.fromJson(Map<String, dynamic> json) {
    return Dermatologist(
      id: json['id'],
      qualification: json['qualification'],
      workEmail: json['work_email'],
      phoneNumber1: json['phone_number_1'],
      phoneNumber2: json['phone_number_2'],
      clinic: json['clinic'],
      locationLat: json['location_lat'].toDouble(),
      locationLon: json['location_lon'].toDouble(),
      locationDesc: json['location_desc'],
      user: User.fromJson(json['user']),
    );
  }
}
