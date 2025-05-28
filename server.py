from flask import Flask, request, jsonify

app = Flask(__name__)

USERS = {
    "admin": "789456123"
    "provosudie": "ebalay1346"
    "cultionpanic": "789456123"
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if USERS.get(username) == password:
        return jsonify({"status": "ok", "message": "Авторизация прошла успешно"})
    else:
        return jsonify({"status": "error", "message": "Неверный логин или пароль"}), 401

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    cmd = data.get('command')
    if cmd == "run":
        return jsonify({"message": "Команда выполнена"})
    elif cmd == "exit":
        return jsonify({"message": "Завершение соединения"})
    else:
        return jsonify({"message": "Неизвестная команда"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
