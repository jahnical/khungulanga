part of 'home_navigation_bloc.dart';

@immutable
abstract class HomeNavigationState {}

class HomeNavigationAppointments extends HomeNavigationState {}

class HomeNavigationScan extends HomeNavigationState {}

class HomeNavigationDermatologists extends HomeNavigationState {}