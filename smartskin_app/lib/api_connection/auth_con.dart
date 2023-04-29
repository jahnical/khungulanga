import 'dart:async';
import 'dart:convert';
import 'dart:developer';
import 'package:dio/dio.dart';
import 'package:smartskin_app/models/auth_user.dart';

const _base = "http://192.168.42.108:8000";
const _tokenEndpoint = "/api-token-auth/";
const _tokenURL = _base + _tokenEndpoint;

Future<Token> getToken(UserLogin userLogin) async {
  final dio = Dio();

  log(_tokenURL);

  final Response response = await dio.post(
    _tokenURL,
    options: Options(headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    }),
    data: jsonEncode(userLogin.toDatabaseJson()),
  );

  if (response.statusCode == 200) {
    return Token.fromJson(response.data);
  } else {
    log(response.data.toString());
    throw Exception(response.data.toString());
  }
}
