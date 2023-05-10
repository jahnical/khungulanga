import 'dart:async';
import 'package:meta/meta.dart';
import 'package:khungulanga_app/api_connection/auth_con.dart';
import 'package:khungulanga_app/dao/user_dao.dart';
import 'package:khungulanga_app/models/auth_user.dart';

AuthUser? USER;
class UserRepository {
  final userDao = UserDao();

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
    return user;
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
    return user;
  }

  Future <void> deleteToken({
    required int id
  }) async {
    await userDao.deleteUser(id);
    USER = null;
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