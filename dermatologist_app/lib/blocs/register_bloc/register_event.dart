part of 'register_bloc.dart';

abstract class RegisterEvent extends Equatable {
  const RegisterEvent();

  @override
  List<Object> get props => [];
}

class RegisterButtonPressed extends RegisterEvent {
  final String firstName;
  final String lastName;
  final String username;
  final String email;
  final String password;
  final String confirmPassword;
  final String phoneNumber;
  final String qualification;
  final String clinic;
  final double locationLat;
  final double locationLon;
  final String locationDesc;

  const RegisterButtonPressed({
    required this.firstName,
    required this.lastName,
    required this.username,
    required this.password,
    required this.confirmPassword,
    required this.email,
    required this.qualification,
    required this.phoneNumber,
    required this.clinic,
    required this.locationLat,
    required this.locationLon,
    required this.locationDesc,
  });

  @override
  List<Object> get props => [
    firstName,
    lastName,
    username,
    password,
    confirmPassword,
    phoneNumber,
    qualification,
    email,
    clinic,
    locationLat,
    locationLon,
    locationDesc
  ];

  @override
  String toString() => 'RegisterButtonPressed { firstName: $firstName, lastName: $lastName, username: $username, password: $password, confirmPassword: $confirmPassword, email: $email }';
}
