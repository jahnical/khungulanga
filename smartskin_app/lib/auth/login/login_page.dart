import 'package:flutter/material.dart';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:smartskin_app/auth/auth/bloc/auth_bloc.dart';
import 'package:smartskin_app/auth/login/bloc/login_bloc.dart';
import 'package:smartskin_app/auth/login/login_form.dart';
import 'package:smartskin_app/repositories/user_repository.dart';


class LoginPage extends StatelessWidget {
  final UserRepository userRepository;

  LoginPage({Key? key, required this.userRepository})
      : assert(userRepository != null),
        super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login | Home Hub'),
      ),
      body: BlocProvider(
        create: (context) {
          return LoginBloc(
            authenticationBloc: BlocProvider.of<AuthBloc>(context),
            userRepository: userRepository,
          );
        },
        child: LoginForm(),
      ),
    );
  }
}