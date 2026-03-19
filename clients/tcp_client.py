import socket
import json


def main():
    host = "localhost"
    port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Подключено к серверу {host}:{port}")

        while True:
            message = input("Введите сообщение (или 'exit' для выхода): ")
            if message.lower() == "exit":
                break

            req = {"message": message}
            s.sendall((json.dumps(req) + "\n").encode("utf-8"))

            data = s.recv(1024).decode("utf-8").strip()
            resp = json.loads(data)

            print(f"Ответ сервера: {resp['message']}")
            print(f"Время сервера: {resp['timestamp']}")


if __name__ == "__main__":
    main()
