import 'dart:async';

import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';
import 'package:smartskin_app/auth/auth/bloc/auth_bloc.dart';
import 'package:smartskin_app/repositories/user_repository.dart';

part 'register_event.dart';
part 'register_state.dart';

class RegisterBloc extends Bloc<RegisterEvent, RegisterState> {
  final UserRepository userRepository;
  final AuthBloc authenticationBloc;

  RegisterBloc({
    required this.userRepository,
    required this.authenticationBloc,
  }) : super(RegisterInitial());

  @override
  Stream<RegisterState> mapEventToState(
    RegisterEvent event,
  ) async* {
    if (event is RegisterButtonPressed) {
      yield RegisterLoading();

      try {
        await userRepository.register(
          username: event.username,
          email: event.email,
          password: event.password,
          dob: event.dateOfBirth,
          firstName: event.firstName,
          lastName: event.lastName,
          gender: event.gender,
        );

        final user = await userRepository.authenticate(
          username: event.username,
          password: event.password,
        );

        authenticationBloc.add(LoggedIn(user: user));
        yield RegisterInitial();
      } catch (error) {
        yield RegisterFailure(error: error.toString());
      }
    }
  }
}
