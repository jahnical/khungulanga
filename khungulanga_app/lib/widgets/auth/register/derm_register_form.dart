import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:intl/intl.dart';
import 'package:khungulanga_app/blocs/register_bloc/register_bloc.dart';

class RegisterDermForm extends StatefulWidget {
  const RegisterDermForm({Key? key}) : super(key: key);

  @override
  State<RegisterDermForm> createState() =>
      _RegisterDermFormState();
}

class _RegisterDermFormState extends State<RegisterDermForm> {
  final _formKey = GlobalKey<FormState>();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  final _qualificationController = TextEditingController();
  final _emailController = TextEditingController();
  final _firstNameController = TextEditingController();
  final _phoneNumber2Controller = TextEditingController();
  final _clinicController = TextEditingController();
  final _locationLatController = TextEditingController();
  final _locationLonController = TextEditingController();
  final _locationDescController = TextEditingController();
  final _lastNameController = TextEditingController();

  _onLoginButtonPressed() {
    Navigator.pop(context);
  }

  _onRegisterButtonPressed() {
    if (_formKey.currentState?.validate() == true) {
      BlocProvider.of<RegisterBloc>(context).add(RegisterButtonPressedDerm(
        username: _emailController.text,
        password: _passwordController.text,
        confirmPassword: _confirmPasswordController.text,
        qualification: _qualificationController.text,
        email: _emailController.text,
        firstName: _firstNameController.text,
        lastName: _lastNameController.text,
        phoneNumber: _phoneNumber2Controller.text,
        clinic: _clinicController.text,
        locationLat: double.parse(_locationLatController.text),
        locationLon: double.parse(_locationLonController.text),
        locationDesc: _locationDescController.text,
      ));
    }
  }

  @override
  Widget build(BuildContext context) {
    return BlocListener<RegisterBloc, RegisterState>(
      listener: (context, state) {
        if (state is RegisterFailure) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text(state.error),
            backgroundColor: Colors.red,
          ));
        }
      },
      child: BlocBuilder<RegisterBloc, RegisterState>(
        builder: (context, state) {
          return SingleChildScrollView(
            child: Form(
              key: _formKey,
              child: Padding(
                padding: EdgeInsets.all(40.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: <Widget>[
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'First Name',
                        icon: Icon(Icons.person),
                      ),
                      controller: _firstNameController,
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter your first name';
                        }
                        return null;
                      },
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'Last Name',
                        icon: Icon(Icons.person),
                      ),
                      controller: _lastNameController,
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter your last name';
                        }
                        return null;
                      },
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'Qualification',
                        icon: Icon(Icons.school),
                      ),
                      controller: _qualificationController,
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter your qualification';
                        }
                        return null;
                      },
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'Email',
                        icon: Icon(Icons.email),
                      ),
                      controller: _emailController,
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter your work email';
                        }
                        return null;
                      },
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'Phone Number',
                        icon: Icon(Icons.phone),
                      ),
                      controller: _phoneNumber2Controller,
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'Clinic',
                        icon: Icon(Icons.home),
                      ),
                      controller: _clinicController,
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter your clinic';
                        }
                        return null;
                      },
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'Location Latitude',
                        icon: Icon(Icons.location_on),
                      ),
                      controller: _locationLatController,
                      keyboardType: TextInputType.number,
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter the location latitude';
                        }
                        return null;
                      },
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'Location Longitude',
                        icon: Icon(Icons.location_on),
                      ),
                      controller: _locationLonController,
                      keyboardType: TextInputType.number,
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter the location longitude';
                        }
                        return null;
                      },
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'Location Description',
                        icon: Icon(Icons.location_on),
                      ),
                      controller: _locationDescController,
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter the location description';
                        }
                        return null;
                      },
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'Password',
                        icon: Icon(Icons.security),
                      ),
                      controller: _passwordController,
                      obscureText: true,
                      validator: (value) {
                        if (value == null ||
                            value.isEmpty ||
                            value.length < 8) {
                          return 'Please enter a password of at least 8 characters';
                        }
                        return null;
                      },
                    ),
                    TextFormField(
                      decoration: const InputDecoration(
                        labelText: 'Confirm password',
                        icon: Icon(Icons.security),
                      ),
                      controller: _confirmPasswordController,
                      obscureText: true,
                      validator: (value) {
                        if (value == null ||
                            value.isEmpty ||
                            value.length < 8) {
                          return 'Please enter a password of at least 8 characters';
                        } else if (value != _passwordController.text) {
                          return 'Passwords do not match';
                        }
                        return null;
                      },
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
                          child: state is RegisterLoading
                              ? const CircularProgressIndicator()
                              : const Text(
                            'Register',
                            style: TextStyle(
                              fontSize: 24.0,
                            ),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(
                      height: 20.0,
                    ),
                    TextButton(
                      onPressed: _onLoginButtonPressed,
                      child: const Text('Login'),
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
