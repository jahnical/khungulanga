import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:dermatologist_app/blocs/auth_bloc/auth_bloc.dart';
import 'package:dermatologist_app/blocs/register_bloc/register_bloc.dart';
import 'package:dermatologist_app/repositories/user_repository.dart';
import 'package:dermatologist_app/widgets/auth/register/register_form.dart';

class RegisterPage extends StatelessWidget {
  final UserRepository userRepository;

  const RegisterPage({Key? key, required this.userRepository})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Register'),
      ),
      body: BlocProvider(
        create: (context) {
          return RegisterBloc(
              authenticationBloc: BlocProvider.of<AuthBloc>(context),
              userRepository: userRepository,
              context: context);
        },
        child: RegisterForm(),
      ),
    );
  }
}
