import 'dart:async';
import 'dart:convert';
import 'dart:developer';
import 'package:dio/dio.dart';
import 'package:smartskin_app/models/diagnosis.dart';
import 'package:smartskin_app/models/prediction.dart';
import 'package:smartskin_app/util/endpoints.dart';

import '../repositories/user_repository.dart';

Options postOptions() {
  return Options(headers: <String, String>{
    'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': 'Token ${USER?.token}'
  });
}

Options getOptions() {
  return Options(headers: <String, String> {
    "Authorization": 'Token ${USER?.token}'
  });
}


