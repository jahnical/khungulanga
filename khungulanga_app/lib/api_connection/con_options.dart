import 'package:dio/dio.dart';
import 'package:khungulanga_app/repositories/user_repository.dart';


/*Options postptions = Options(headers: <String, String>{
  'Content-Type': 'application/json; charset=UTF-8',
  'Authorization': 'Token ${USER?.token}'
});
Options getOptions = Options(headers: <String, String> {
  "Authorization": 'Token ${USER?.token}'
});*/

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