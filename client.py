import threading
import time
import socket
import os

SERVER_PORT = int(input("Введите порт сервера: "))
CLIENT_PORT = int(input("Введите порт клиента: "))
ip = str(input("Введите IP-адрес сервера: "))


# ----------------------------------------------------------------------

def all_die():
    client.die()
    server.die()

class Client(threading.Thread):
    def die(self):
        self.client_socket.close()
        print("Клиентский сокет закрыт")

    def run(self):
        self.isRunning = True
        try:
            while True:
                message = str(input("Сообщение: "))
                self.client_socket.send(message.encode())
        except Exception as e:
            print(e)

    def __init__(self, server_ip, port):
        threading.Thread.__init__(self)
        self.client_socket = socket.socket()
        while True:
            try:
                self.client_socket.connect((server_ip, port))
                time.sleep(1)
                print("Подключились")
                break
            except:
                print("Не подключились")
                continue
        self.setDaemon(False    )
        self.isRunning = False


class Server(threading.Thread):
    def die(self):
        self.server_socket.close()
        print("Серверный сокет закрыт")

    def run(self):
        conn, addr = self.server_socket.accept()
        while True:
            try:
                message = conn.recv(16384).decode()
                if message:
                    print("Принято: " + message + "\n")
                else:
                    print("Получено пустое сообщение")
                    all_die()
            except Exception as e:
                print(e)
                self.die()
                break

    def __init__(self, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.server_socket = socket.socket()
        self.server_socket.bind(("", port))
        self.server_socket.listen(100)


# ----------------------------------------------------------------------


print("Начинаем работу...")

server = Server(SERVER_PORT)
server.start()
client = Client(ip, CLIENT_PORT)
client.start()
