import 'dart:async';
import 'dart:developer';
import 'package:dio/dio.dart';
import 'package:smartskin_app/models/prediction.dart';
import 'package:smartskin_app/util/endpoints.dart';

import '../repositories/user_repository.dart';

Options options = Options(headers: <String, String>{
  'Content-Type': 'application/json; charset=UTF-8',
  'Authorization': 'Token ${USER?.token}'
});

Future<List<Prediction>> getPredictions(FormData data) async {
  final dio = Dio();

  log(DIAGNOSIS_URL);

  final Response response = await dio.post(
    DIAGNOSIS_URL,
    options: options,
    data: data,
  );

  if (response.statusCode == 201) {
    return (response.data as List).map((e) => Prediction.fromJson(e)).toList();
  } else {
    log(response.data.toString());
    throw Exception(response.data.toString());
  }
}
