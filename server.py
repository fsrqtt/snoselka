from flask import Flask, request, jsonify
import os

app = Flask(__name__)

USERS = {
    "admin": "789456123",
    "Skizzy": "Skizzy13371337",
    "cultionpanic": "789456123"
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"status": "error", "message": "Логин и пароль обязательны"}), 400
    if username in USERS and USERS[username] == password:
        return jsonify({"status": "ok", "message": f"Добро пожаловать, {username}!"}), 200
    else:
        return jsonify({"status": "error", "message": "Неверный логин или пароль"}), 401

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
