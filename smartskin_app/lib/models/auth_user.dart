class User {
  int id;
  String username;
  String token;

  User({required this.id,
      required this.username,
      required this.token});

  factory User.fromDatabaseJson(Map<String, dynamic> data) => User(
      id: data['id'],
      username: data['username'],
      token: data['token'],
  );

  Map<String, dynamic> toDatabaseJson() => {
        "id": id,
        "username": username,
        "token": token
      };
}

class UserLogin {
  String username;
  String password;

  UserLogin({required this.username, required this.password});

  Map <String, dynamic> toDatabaseJson() => {
    "username": username,
    "password": password
  };
}

class Token{
  String token;

  Token({required this.token});

  factory Token.fromJson(Map<String, dynamic> json) {
    return Token(
      token: json['token']
    );
  }
}