import 'dart:async';
import 'package:dio/dio.dart';
import 'package:khungulanga_app/models/patient.dart';
import 'package:khungulanga_app/models/user.dart';
import 'package:meta/meta.dart';
import 'package:khungulanga_app/api_connection/auth_con.dart';
import 'package:khungulanga_app/dao/user_dao.dart';
import 'package:khungulanga_app/models/auth_user.dart';

import '../api_connection/api_client.dart';
import '../api_connection/con_options.dart';
import '../api_connection/endpoints.dart';

AuthUser? USER;
class UserRepository {
  final userDao = UserDao();
  Patient? patient;
  final _dio = APIClient.dio;

  Future<AuthUser> authenticate ({
    required String username,
    required String password,
  }) async {
    UserLogin userLogin = UserLogin(
        username: username,
        password: password
    );
    Token token = await getToken(userLogin);
    AuthUser user = AuthUser(
      id: 0,
      username: username,
      token: token.token,
    );
    fetchPatient(user.username);
    return user;
  }

  Future<Patient> fetchPatient(String username) async {
    if (this.patient != null) return this.patient!;
    final response = await _dio.get('$PATIENTS_URL/$username/', options: getOptions());
    final patientJson = response.data as Map<String, dynamic>;
    final patient = Patient.fromJson(patientJson);
    this.patient = patient;
    return patient;
  }

  Future<void> persistToken ({
    required AuthUser user
  }) async {
    // write token with the user to the database
    await userDao.createUser(user);
  }

  Future<AuthUser?> getUserFromDB() async {
    AuthUser? user = await userDao.getToken(0);
    USER = user;
    if (user != null) {
      fetchPatient(user.username);
    }
    return user;
  }

  Future <void> deleteToken({
    required int id
  }) async {
    await userDao.deleteUser(id);
    USER = null;
    this.patient = null;
  }

  Future <bool> hasToken() async {
    bool result = await userDao.checkUser(0);
    return result;
  }

  Future<UserRegister> register(
      {required String username,
      required String email,
      required String password,
      required String firstName,
      required String lastName,
      required DateTime dob,
      required String gender}) async {
    // create a UserRegister object with the necessary fields
    final userRegister = UserRegister(
        username: username,
        password: password,
        firstName: firstName,
        lastName: lastName,
        dob: dob,
        email: email,
        gender: gender);

    await registerUser(userRegister);
    
    return userRegister;
  }
}