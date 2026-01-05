import socket
import threading
import logging

logging.basicConfig(level = logging.INFO)

clients = set()
lock = threading.Lock()

def broadcast(message):
    dead = []
    with lock:
        for client in clients:
            try:
                client.sendall(f"{message}\n".encode())
            except Exception as e:
                logging.error(f"Error sending message to client: {e}")
                dead.append(client)
        for client in dead:
            clients.discard(client)
                

def handle_client(client_socket):
    with lock:
        clients.add(client_socket)
    try:
        client_socket.sendall(b"Welcome to the chatroom!\n")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode().strip()
            if message:
                broadcast(message)
    finally:
        with lock:
            clients.discard(client_socket)
        client_socket.close()
        


def start_server(HOST, PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    logging.info(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        logging.info(f"Accepted connection from {address}")
        client_socket_thread = threading.Thread(target = handle_client, args = (client_socket,))
        client_socket_thread.start()

if __name__ == "__main__":
    start_server(HOST = "localhost", PORT = 1337)