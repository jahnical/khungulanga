import 'dart:convert';
import 'dart:developer';

import 'package:dio/dio.dart';
import 'package:khungulanga_app/models/diagnosis.dart';
import 'package:khungulanga_app/util/endpoints.dart';

import '../api_connection/con_options.dart';

class DiagnosisRepository {
  final Dio _dio = Dio();

  Future<List<Diagnosis>> fetchDiagnoses() async {
    try {
      final response = await _dio.get("$DIAGNOSIS_URL/", options: getOptions());
      final data = response.data as List<dynamic>;
      final diagnoses = data.map((e) => Diagnosis.fromJson(e)).toList();
      return diagnoses;
    } on DioError catch (e) {
      throw Exception(e.message);
    }
  }

  Future<Diagnosis> diagnose(FormData data) async {
    final dio = Dio();

    log(DIAGNOSIS_URL);

    try {
      final Response response = await dio.post(
        "$DIAGNOSIS_URL/",
        options: postOptions(),
        data: data,
      );
      if (response.statusCode == 200) {
        return Diagnosis.fromJson(response.data);
      } else {
        log(response.data.toString());
        throw Exception(response.data.toString());
      }
    } on DioError catch (e) {
      log(e.toString());
      if (e.response?.statusCode == 400) {
        throw Exception("No skin detected, make sure the image is clear and the skin covers at least half of it.");
      }
      rethrow;
    }
  }

  Future<bool> delete(id) async {
    try {
      await _dio.delete("$DIAGNOSIS_URL/$id", options: getOptions());
      return true;
    } on DioError catch (e) {
      throw Exception(e.message);
    }
  }
}
