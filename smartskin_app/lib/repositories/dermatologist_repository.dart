
import 'package:dio/dio.dart';
import 'package:smartskin_app/models/dermatologist.dart';
import 'package:smartskin_app/util/endpoints.dart';

class DermatologistRepository {
  final Dio _dio = Dio();

  Future<List<Dermatologist>> getDermatologists() async {
    final response = await _dio.get(DERMATOLOGISTS_URL);
    final dermatologistsJson = response.data as List<dynamic>;
    final dermatologists = dermatologistsJson
        .map((json) => Dermatologist.fromJson(json as Map<String, dynamic>))
        .toList();
    return dermatologists;
  }

  Future<Dermatologist> getDermatologistById(int id) async {
    final response = await _dio.get('$DERMATOLOGISTS_URL/$id');
    final dermatologistJson = response.data as Map<String, dynamic>;
    final dermatologist = Dermatologist.fromJson(dermatologistJson);
    return dermatologist;
  }

  /*Future<Dermatologist> createDermatologist(Dermatologist dermatologist) async {
    final response = await _dio.post('https://example.com/dermatologists',
        data: jsonEncode(dermatologist.toJson()));
    final dermatologistJson = response.data as Map<String, dynamic>;
    final createdDermatologist = Dermatologist.fromJson(dermatologistJson);
    return createdDermatologist;
  }

  Future<void> updateDermatologist(int id, Dermatologist dermatologist) async {
    await _dio.put('https://example.com/dermatologists/$id',
        data: jsonEncode(dermatologist.toJson()));
  }*/

  Future<void> deleteDermatologist(int id) async {
    await _dio.delete('$DERMATOLOGISTS_URL/$id');
  }

  Future<List<Dermatologist>> getNearbyDermatologists(latitude, longitude) async {
    final response = await _dio.get('$DERMATOLOGISTS_URL/nearby?latitude=$latitude&longitude=$longitude', options: getOptions());
    final dermatologistsJson = response.data as List<dynamic>;
    final dermatologists = dermatologistsJson
        .map((json) => Dermatologist.fromJson(json as Map<String, dynamic>))
        .toList();
    return dermatologists;
  }
}