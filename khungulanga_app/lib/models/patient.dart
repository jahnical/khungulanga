import 'package:khungulanga_app/models/user.dart';

class Patient {
  final int id;
  final String username;
  final String password;
  final String firstName;
  final String lastName;
  final String email;
  final DateTime dob;
  final String gender;
  bool? isStaff =false;
  bool? isActive = false;
  DateTime? lastLogin;
  DateTime? dateJoined;
  User? user;

  Patient({
    required this.id,
    required this.username,
    required this.password,
    required this.firstName,
    required this.lastName,
    required this.email,
    required this.dob,
    required this.gender,
    this.isStaff,
    this.isActive,
    this.lastLogin,
    this.dateJoined,
  });

  factory Patient.fromJson(Map<String, dynamic> json) {
    return Patient(
      id: json['id'],
      username: json['username'],
      password: json['password'],
      firstName: json['first_name'],
      lastName: json['last_name'],
      email: json['email'],
      isStaff: json['is_staff'],
      isActive: json['is_active'],
      lastLogin: DateTime.parse(json['last_login']),
      dateJoined: DateTime.parse(json['date_joined']),
      dob: DateTime.parse(json['dob']),
      gender: json['gender'],
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'username': username,
        'password': password,
        'first_name': firstName,
        'last_name': lastName,
        'email': email,
        'is_staff': isStaff,
        'is_active': isActive,
        'last_login': lastLogin?.toIso8601String(),
        'date_joined': dateJoined?.toIso8601String(),
        'dob': dob.toIso8601String(),
        'gender': gender,
      };
}
