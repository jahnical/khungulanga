import 'dart:async';
import 'package:dermatologist_app/models/patient.dart';
import 'package:dermatologist_app/api_connection/auth_con.dart';
import 'package:dermatologist_app/dao/user_dao.dart';
import 'package:dermatologist_app/models/auth_user.dart';

import '../api_connection/api_client.dart';
import '../api_connection/con_options.dart';
import '../api_connection/endpoints.dart';
import '../models/dermatologist.dart';

AuthUser? USER;

class UserRepository {
  final userDao = UserDao();
  Dermatologist? dermatologist;
  final _dio = APIClient.dio;

  Future<AuthUser> authenticate({
    required String username,
    required String password,
  }) async {
    UserLogin userLogin = UserLogin(username: username, password: password);
    Token token = await getToken(userLogin);
    AuthUser user = AuthUser(
      id: 0,
      username: username,
      token: token.token,
    );
    fetchDermatologist(user.username);
    return user;
  }

  Future<Dermatologist> fetchDermatologist(String username) async {
    if (this.dermatologist != null) return this.dermatologist!;
    final response =
        await _dio.get('$DERMATOLOGISTS_URL/$username/', options: getOptions());
    final dermatologistJson = response.data as Map<String, dynamic>;
    final dermatologist = Dermatologist.fromJson(dermatologistJson);
    this.dermatologist = dermatologist;
    return dermatologist;
  }

  Future<void> persistToken({required AuthUser user}) async {
    // write token with the user to the database
    await userDao.createUser(user);
  }

  Future<AuthUser?> getUserFromDB() async {
    AuthUser? user = await userDao.getToken(0);
    USER = user;
    if (user != null) {
      fetchDermatologist(user.username);
    }
    return user;
  }

  Future<void> deleteToken({required int id}) async {
    await userDao.deleteUser(id);
    USER = null;
    this.dermatologist = null;
  }

  Future<bool> hasToken() async {
    bool result = await userDao.checkUser(0);
    return result;
  }

  Future<UserRegister> register(
      {required String username,
      required String email,
      required String password,
      required String firstName,
      required String lastName,
        required String phoneNumber,
        required String qualification,
        required String clinic,
        required double locationLat,
        required double locationLon,
        required String locationDesc,
      }) async {
    // create a UserRegister object with the necessary fields
    final userRegister = UserRegister(
        username: username,
        password: password,
        firstName: firstName,
        lastName: lastName,
        email: email,
        phoneNumber:   phoneNumber,
        qualification: qualification,
        clinic:        clinic,
        locationLat:   locationLat,
        locationLon:   locationLon,
        locationDesc:  locationDesc,
    );

    await registerUser(userRegister);

    return userRegister;
  }
}
