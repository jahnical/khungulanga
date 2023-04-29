import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:smartskin_app/auth/auth/bloc/auth_bloc.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home | Home Hub'),
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          const Padding(padding: EdgeInsets.only(left: 30.0),
          child: Text(
            'Welcome',
            style: TextStyle(
              fontSize: 24.0,
            ),
          ),),
          Padding(
            padding: const EdgeInsets.fromLTRB(34.0, 20.0, 0.0, 0.0),
            child: SizedBox(
              width: MediaQuery.of(context).size.width * 0.85,
              height: MediaQuery.of(context).size.width * 0.16,
              child: FloatingActionButton(
                onPressed: () {
                  BlocProvider.of<AuthBloc>(context)
                      .add(LoggedOut());
                },
                shape: const StadiumBorder(
                  side: BorderSide(
                    color: Colors.black,
                    width: 2,
                  ),
                ),
                child: const Text(
                  'Logout',
                  style: TextStyle(
                    fontSize: 24,
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}