import 'dart:async';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:meta/meta.dart';
import 'package:equatable/equatable.dart';
import 'package:smartskin_app/models/auth_user.dart';
import 'package:smartskin_app/repositories/user_repository.dart';

part 'auth_event.dart';
part 'auth_state.dart';

class AuthBloc
    extends Bloc<AuthEvent, AuthState> {
  final UserRepository userRepository;

  AuthBloc({required this.userRepository}) : super(AuthUnintialized());

  @override
  AuthState get initialState => AuthUnintialized();

  @override
  Stream<AuthState> mapEventToState(
    AuthEvent event,
  ) async* {
    if (event is AppStarted) {

      final bool hasToken = await userRepository.hasToken();

      if (hasToken) {
        yield AuthAuthenticated();
      } else {
        yield AuthUnauthenticated();
      }
    }

    if (event is LoggedIn) {
      yield AuthLoading();

      await userRepository.persistToken(
        user: event.user
      );
      yield AuthAuthenticated();
    }

    if (event is LoggedOut) {
      yield AuthLoading();

      await userRepository.deleteToken(id: 0);

      yield AuthUnauthenticated();
    }
  }
}