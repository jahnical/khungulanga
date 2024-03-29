import 'dart:async';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meta/meta.dart';
import 'package:equatable/equatable.dart';
import 'package:dermatologist_app/models/auth_user.dart';
import 'package:dermatologist_app/repositories/user_repository.dart';
import 'package:flutter/foundation.dart' show kIsWeb;

part 'auth_event.dart';
part 'auth_state.dart';

class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final UserRepository userRepository;

  AuthBloc({required this.userRepository}) : super(AuthUninitialized());

  @override
  AuthState get initialState => AuthUninitialized();

  @override
  Stream<AuthState> mapEventToState(
    AuthEvent event,
  ) async* {
    if (event is AppStarted) {
      //For web testing
      if (kIsWeb) {
        yield AuthAuthenticated(null);
        return;
      }
      userRepository.getUserFromDB();
      final bool hasToken = await userRepository.hasToken();

      if (hasToken) {
        yield AuthAuthenticated(await userRepository.getUserFromDB());
      } else {
        yield AuthUnauthenticated();
      }
    }

    if (event is LoggedIn) {
      yield AuthLoading();

      await userRepository.persistToken(user: event.user);
      yield AuthAuthenticated(await userRepository.getUserFromDB());
    }

    if (event is LoggedOut) {
      yield AuthLoading();

      await userRepository.deleteToken(id: 0);

      yield AuthUnauthenticated();
    }
  }
}
