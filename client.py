import socket

HOST = 'your_server_ip'  # Replace with the server's public IP
PORT = 12345

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        while True:
            message = client.recv(1024).decode()
            print(message)
            if "логин" in message:
                username = input()
                client.send(username.encode())
            elif "пароль" in message:
                password = input()
                client.send(password.encode())
            elif "команду" in message:
                command = input("Введите команду (run/exit): ")
                client.send(command.encode())
            elif "Завершение соединения" in message:
                break
            elif "Неверный логин или пароль" in message:
                break
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()