import 'dart:async';

import 'package:bloc/bloc.dart';
import 'package:meta/meta.dart';

part 'home_navigation_event.dart';
part 'home_navigation_state.dart';

class HomeNavigationBloc extends Bloc<HomeNavigationEvent, HomeNavigationState> {
  HomeNavigationBloc() : super(HomeNavigationAppointments()) {
    on<HomeNavigationEvent>((event, emit) {
      if (event is NavigateToHistory) {
        emit(HomeNavigationAppointments());
      } else if (event is NavigateToScan) {
        emit(HomeNavigationScan());
      } else if (event is NavigateToDermatologists) {
        emit(HomeNavigationDermatologists());
      }
    });
  }
}
