import 'package:intl/intl.dart';

class AuthUser {
  int id;
  String username;
  String token;

  AuthUser({required this.id,
      required this.username,
      required this.token});

  factory AuthUser.fromDatabaseJson(Map<String, dynamic> data) => AuthUser(
      id: data['id'],
      username: data['username'],
      token: data['token'],
  );

  Map<String, dynamic> toDatabaseJson() => {
        "id": id,
        "username": username,
        "token": token
      };
}

class UserLogin {
  String username;
  String password;

  UserLogin({required this.username, required this.password});

  Map <String, dynamic> toDatabaseJson() => {
    "username": username,
    "password": password
  };
}

class Token{
  String token;

  Token({required this.token});

  factory Token.fromJson(Map<String, dynamic> json) {
    return Token(
      token: json['token']
    );
  }
}

class UserRegister {
  String username;
  String password;
  String email;
  String firstName;
  String lastName;
  final String phoneNumber;
  final String qualification;
  final String clinic;
  final double locationLat;
  final double locationLon;
  final String locationDesc;


  UserRegister({
    required this.username,
    required this.password,
    required this.email,
    required this.firstName,
    required this.lastName,
    required this.qualification,
    required this.phoneNumber,
    required this.clinic,
    required this.locationLat,
    required this.locationLon,
    required this.locationDesc,
  });

  Map<String, dynamic> toDatabaseJson() => {
        "username": username,
        "password": password,
        "email": email,
        "first_name": firstName,
        "last_name": lastName,
        "qualification": qualification,
        "phone_number": phoneNumber,
        "clinic": clinic,
        "location_lat": locationLat,
        "location_lon": locationLon,
        "location_desc": locationDesc
      };
}
