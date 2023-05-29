part of 'home_navigation_bloc.dart';

@immutable
abstract class HomeNavigationEvent {}

class NavigateToAppointments extends HomeNavigationEvent {}

class NavigateToScan extends HomeNavigationEvent {}

class NavigateToChats extends HomeNavigationEvent {}