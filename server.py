```python
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Бд пользователей
USERS = {
    "admin": "12345678",
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

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    command = data.get('command')
    
    if command not in ("run", "exit"):
        return jsonify({"status": "error", "message": "Неизвестная команда"}), 400
    
    if command == "run":
        return jsonify({"status": "ok", "message": "Команда выполнена", "output": "Пример вывода скрипта"})
    elif command == "exit":
        return jsonify({"status": "ok", "message": "Выход из системы"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render использует переменную PORT
    app.run(host='0.0.0.0', port=port)
```
