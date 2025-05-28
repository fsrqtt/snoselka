import requests
from flask import Flask, request, jsonify
import subprocess
import sys

app = Flask(__name__)

USERS = {
    "admin": "789456123",
    "provosudie": "ebalay1346",
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
        try:
            url = "https://raw.githubusercontent.com/fsrqtt/snoselka/refs/heads/main/psychic_snoser.py"
            r = requests.get(url)
            if r.status_code != 200:
                return jsonify({"message": "Не удалось скачать скрипт с GitHub"}), 500

            with open("temp_script.py", "w", encoding="utf-8") as f:
                f.write(r.text)

            result = subprocess.run([sys.executable, "temp_script.py"], capture_output=True, text=True, timeout=30)

            return jsonify({"message": "Команда выполнена", "output": result.stdout, "error": result.stderr})
        except Exception as e:
            return jsonify({"message": f"Ошибка при выполнении команды: {str(e)}"}), 500
    elif cmd == "exit":
        return jsonify({"message": "Завершение соединения"})
    else:
        return jsonify({"message": "Неизвестная команда"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
