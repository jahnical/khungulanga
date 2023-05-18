part of 'auth_bloc.dart';

@immutable
abstract class AuthState extends Equatable {
  @override
  List<Object> get props => [];
}

class AuthUninitialized extends AuthState {}

class AuthAuthenticated extends AuthState {
  final AuthUser? authUser;
  AuthAuthenticated(this.authUser);
}

class AuthUnauthenticated extends AuthState {}

class AuthLoading extends AuthState {}