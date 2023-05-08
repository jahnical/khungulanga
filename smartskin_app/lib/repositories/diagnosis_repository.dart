import 'dart:convert';
import 'dart:developer';

import 'package:dio/dio.dart';
import 'package:smartskin_app/models/diagnosis.dart';
import 'package:smartskin_app/util/endpoints.dart';

import '../api_connection/diagnosis_con.dart';

class DiagnosisRepository {
  final Dio _dio = Dio();

  Future<List<Diagnosis>> fetchDiagnoses() async {
    try {
      final response = await _dio.get('https://your-api.com/diagnoses');
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
        DIAGNOSIS_URL,
        options: options,
        data: data,
      );
      if (response.statusCode == 200) {
        return Diagnosis.fromJson(jsonDecode(response.data));
      } else {
        log(response.data.toString());
        throw Exception(response.data.toString());
      }
    } on DioError catch (e) {
      log(e.toString());
      if (e.response?.statusCode == 400) {
        throw Exception("No skin detected, make sure the image is clear and the skin covers at least half it.");
      }
      rethrow;
    }
  }
}
