import 'package:intl/intl.dart';

class User {
  int id;
  String username;
  String token;

  User({required this.id,
      required this.username,
      required this.token});

  factory User.fromDatabaseJson(Map<String, dynamic> data) => User(
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
  DateTime dob;
  String gender;

  UserRegister({
    required this.username,
    required this.password,
    required this.email,
    required this.firstName,
    required this.lastName,
    required this.dob,
    required this.gender,
  });

  Map<String, dynamic> toDatabaseJson() => {
        "username": username,
        "password": password,
        "email": email,
        "first_name": firstName,
        "last_name": lastName,
        "dob": dob.toIso8601String(),
        "gender": gender,
      };
}
