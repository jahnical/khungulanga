import 'package:bloc/bloc.dart';
import 'package:meta/meta.dart';
import '../../models/diagnosis.dart';
import '../../repositories/diagnosis_repository.dart';
part 'diagnosis_event.dart';
part 'diagnosis_state.dart';

class DiagnosisBloc extends Bloc<DiagnosisEvent, DiagnosisState> {
  final DiagnosisRepository _repository;

  DiagnosisBloc({required DiagnosisRepository repository})
      : _repository = repository,
        super(DiagnosisInitial());

  @override
  Stream<DiagnosisState> mapEventToState(DiagnosisEvent event) async* {
    if (event is FetchDiagnoses) {
      yield DiagnosisLoading();

      try {
        final diagnoses = await _repository.fetchDiagnoses();
        yield DiagnosisLoaded(diagnoses: diagnoses);
      } catch (e) {
        yield DiagnosisError(message: 'Failed to load diagnoses');
      }
    } else if (event is DeleteDiagnosis) {
      yield DiagnosisDeleting();

      try {
        await _repository.delete(event.diagnosis.id!);
        final diagnoses = await _repository.fetchDiagnoses();
        yield DiagnosisDeleted(diagnoses: diagnoses);
      } catch (e) {
        yield DiagnosisError(message: 'Failed to delete diagnosis');
      }
    }
  }
}