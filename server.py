import socket
import threading
import json
from psychic_snoser import main  # Import the main function from the main script

# Server configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12345      # Arbitrary port number
ADMIN_CREDENTIALS = {"username": "admin", "password": "snoser123"}

def handle_client(client_socket):
    try:
        # Authenticate client
        client_socket.send("Введите логин: ".encode())
        username = client_socket.recv(1024).decode().strip()
        client_socket.send("Введите пароль: ".encode())
        password = client_socket.recv(1024).decode().strip()

        if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
            client_socket.send("Авторизация успешна! Введите команду (run/exit): ".encode())
        else:
            client_socket.send("Неверный логин или пароль!".encode())
            client_socket.close()
            return

        while True:
            command = client_socket.recv(1024).decode().strip()
            if command == "run":
                client_socket.send("Запуск Психического Сносера...".encode())
                main()  # Call the main function from psychic_snoser.py
                client_socket.send("Выполнение завершено. Введите следующую команду: ".encode())
            elif command == "exit":
                client_socket.send("Завершение соединения.".encode())
                break
            else:
                client_socket.send("Неизвестная команда. Доступные команды: run, exit".encode())
    except Exception as e:
        client_socket.send(f"Ошибка на сервере: {str(e)}".encode())
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Сервер запущен на {HOST}:{PORT}")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Подключен клиент: {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()