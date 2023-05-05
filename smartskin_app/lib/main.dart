import 'dart:developer';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:smartskin_app/auth/auth/bloc/auth_bloc.dart';
import 'package:smartskin_app/auth/login/login_page.dart';
import 'package:smartskin_app/common/common.dart';
import 'package:smartskin_app/home/home_page.dart';
import 'package:smartskin_app/repositories/user_repository.dart';
import 'package:smartskin_app/scan/scan_page.dart';
import 'package:smartskin_app/splash/splash_page.dart';

class SimpleBlocObserver extends BlocObserver {
  @override
  void onEvent(Bloc bloc, Object? event) {
    super.onEvent(bloc, event);
    print(event);
  }

  @override
  void onTransition(Bloc bloc, Transition transition) {
    super.onTransition(bloc, transition);
    print (transition);
  }

  @override
  void onError(BlocBase bloc, Object error, StackTrace stackTrace) {
    super.onError(bloc, error, stackTrace);
  }
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  final firstCamera = cameras.first;
  camera = firstCamera;
  Bloc.observer = SimpleBlocObserver();
  final userRepository = UserRepository();

  runApp(
    BlocProvider<AuthBloc>(
      create: (context) {
        return AuthBloc(
          userRepository: userRepository
        )..add(AppStarted());
      },
      child: App(userRepository: userRepository),
    )
  );
}

class App extends StatelessWidget {
  final UserRepository userRepository;

  const App({Key? key, required this.userRepository}) : super(key: key);

  @override
  Widget build (BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        primarySwatch: Colors.blue,
        brightness: Brightness.dark,
      ),
      home: BlocBuilder<AuthBloc, AuthState>(
        builder: (context, state) {
          log(state.toString());
          if (state is AuthUnintialized) {
            return const SplashPage();
          }
          if (state is AuthUnauthenticated) {
            return LoginPage(userRepository: userRepository,);
          }
          if (state is AuthLoading) {
            return const LoadingIndicator();
          }
          return const HomePage();
        },
      ),
    );
  }
}