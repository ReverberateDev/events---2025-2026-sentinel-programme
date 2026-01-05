import socket
import threading
import time

def connect_ddos_clients(HOST, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(b"DDOS_ATTACKER\n")
    time.sleep(1000)

for _ in range(10):
    threading.Thread(target=connect_ddos_clients, args=("localhost", 1337)).start()