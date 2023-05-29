import 'user.dart';

class Dermatologist {
  int id;
  String qualification;
  String email;
  String phoneNumber;
  String clinic;
  double locationLat;
  double locationLon;
  String locationDesc;
  User user;

  Dermatologist({
    required this.id,
    required this.qualification,
    required this.email,
    required this.phoneNumber,
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
      email: json['email'],
      phoneNumber: json['phone_number'],
      clinic: json['clinic'],
      locationLat: json['location_lat'].toDouble(),
      locationLon: json['location_lon'].toDouble(),
      locationDesc: json['location_desc'],
      user: User.fromJson(json['user']),
    );
  }
}