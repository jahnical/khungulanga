import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:smartskin_app/auth/register/bloc/register_bloc.dart';

class RegisterForm extends StatefulWidget {
  @override
  State<RegisterForm> createState() => _RegisterFormState();
}

class _RegisterFormState extends State<RegisterForm> {
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  final _dobController = TextEditingController();
  final _genderController = TextEditingController();
  final _emailController = TextEditingController();
  final _firstNameController = TextEditingController();
  final _lastNameController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    _onRegisterButtonPressed() {
      BlocProvider.of<RegisterBloc>(context).add(RegisterButtonPressed(
        username: _usernameController.text,
        password: _passwordController.text,
        confirmPassword: _confirmPasswordController.text,
        firstName: _firstNameController.text,
        lastName: _lastNameController.text,
        dateOfBirth: DateTime.parse(_dobController.text),
        gender: _genderController.text, 
        email: _emailController.text,
      ));
    }

    return BlocListener<RegisterBloc, RegisterState>(
      listener: (context, state) {
        if (state is RegisterFailure) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text('${state.error}'),
            backgroundColor: Colors.red,
          ));
        }
      },
      child: BlocBuilder<RegisterBloc, RegisterState>(
        builder: (context, state) {
          return Container(
            child: Form(
              child: Padding(
                padding: EdgeInsets.all(40.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: <Widget>[
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'username',
                        icon: Icon(Icons.person),
                      ),
                      controller: _usernameController,
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'email',
                        icon: Icon(Icons.email),
                      ),
                      controller: _emailController,
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'first name',
                        icon: Icon(Icons.person),
                      ),
                      controller: _firstNameController,
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'last name',
                        icon: Icon(Icons.person),
                      ),
                      controller: _lastNameController,
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'date of birth',
                        icon: Icon(Icons.calendar_today),
                      ),
                      controller: _dobController,
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'gender',
                        icon: Icon(Icons.person),
                      ),
                      controller: _genderController,
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'password',
                        icon: Icon(Icons.security),
                      ),
                      controller: _passwordController,
                      obscureText: true,
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'confirm password',
                        icon: Icon(Icons.security),
                      ),
                      controller: _confirmPasswordController,
                      obscureText: true,
                    ),
                    SizedBox(
                      width: MediaQuery.of(context).size.width * 0.85,
                      height: MediaQuery.of(context).size.width * 0.22,
                      child: Padding(
                        padding: const EdgeInsets.only(top: 30.0),
                        child: ElevatedButton(
                          onPressed: state is! RegisterLoading
                              ? _onRegisterButtonPressed
                              : null,
                          style: ElevatedButton.styleFrom(
                            shape: const StadiumBorder(
                              side: BorderSide(
                                color: Colors.black,
                                width: 2,
                              ),
                            ),
                          ),
                          child: const Text(
                            'Register',
                            style: TextStyle(
                              fontSize: 24.0,
                            ),
                          ),
                        ),
                      ),
                    ),
                    Container(
                      child: state is RegisterLoading
                          ? CircularProgressIndicator()
                          : null,
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
