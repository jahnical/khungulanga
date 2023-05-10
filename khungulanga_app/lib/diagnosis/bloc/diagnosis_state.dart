part of 'diagnosis_bloc.dart';


@immutable
abstract class DiagnosisState {}

class DiagnosisInitial extends DiagnosisState {}

class DiagnosisLoading extends DiagnosisState {}

class DiagnosisLoaded extends DiagnosisState {
  final List<Diagnosis> diagnoses;
  DiagnosisLoaded({required this.diagnoses});
}

class DiagnosisError extends DiagnosisState {
  final String message;
  DiagnosisError({required this.message});
}

class DiagnosisDeleting extends DiagnosisState {}

class DiagnosisDeleted extends DiagnosisState {
  final List<Diagnosis> diagnoses;
  DiagnosisDeleted({required this.diagnoses});
}

class DiagnosisDeletingError extends DiagnosisState {
  final String message;
  DiagnosisDeletingError({required this.message});
}