import 'package:smartskin_app/database/user_database.dart';
import 'package:smartskin_app/models/auth_user.dart';

class UserDao {
  final dbProvider = DatabaseProvider.dbProvider;

  Future<int> createUser(User user) async {
    final db = await dbProvider.database;
    var result = db.insert(userTable, user.toDatabaseJson());
    return result;
  }

  Future<int> deleteUser(int id) async {
    final db = await dbProvider.database;
    var result = await db.delete(userTable, where: "id = ?", whereArgs: [id]);
    return result;
  }

  Future<bool> checkUser(int id) async {
    final db = await dbProvider.database;
    try {
      List<Map> users = await db.query(userTable, where: 'id = ?', whereArgs: [id]);
      return users.isNotEmpty;
    } catch (error) {
      return false;
    }
  }
}