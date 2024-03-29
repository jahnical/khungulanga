import 'package:dio/dio.dart';
import 'package:dermatologist_app/repositories/user_repository.dart';

Options postOptions() {
  return Options(headers: <String, String>{
    'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': 'Token ${USER?.token}'
  });
}

Options getOptions() {
  return Options(
      headers: <String, String>{"Authorization": 'Token ${USER?.token}'});
}

Options patchOptions() {
  return Options(headers: <String, String>{
    'Content-Type': 'application/json; charset=UTF-8',
    "Authorization": 'Token ${USER?.token}'
  });
}

Options putOptions() {
  return Options(headers: <String, String>{
    'Content-Type': 'application/json; charset=UTF-8',
    "Authorization": 'Token ${USER?.token}'
  });
}
