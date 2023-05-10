part of 'diagnosis_bloc.dart';

@immutable
abstract class DiagnosisEvent {}

class FetchDiagnoses extends DiagnosisEvent {}

class AddDiagnosis extends DiagnosisEvent {
  final Diagnosis diagnosis;

  AddDiagnosis(this.diagnosis);
}

class DeleteDiagnosis extends DiagnosisEvent {
  final Diagnosis diagnosis;

  DeleteDiagnosis(this.diagnosis);
}

class UpdateDiagnosis extends DiagnosisEvent {
  final Diagnosis diagnosis;

  UpdateDiagnosis(this.diagnosis);
}
