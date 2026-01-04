import socket
import threading
import logging

logging.basicConfig(level = logging.INFO)

clients = set()
lock = threading.RLock()

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
                
def ddos_catch():
    if len(clients) > 10:
        logging.warning("High number of clients connected! Possible DDoS attack detected.")
        broadcast("Server is experiencing high load. Disconnecting all clients.")
        for client in clients:
            client.close()
        clients.clear()

def handle_client(client_socket):
    with lock:
        clients.add(client_socket)
        ddos_catch()
    try:
        client_socket.sendall(b"Welcome to the chat! What is your name?\n")
        name = client_socket.recv(1024).decode().strip()
        broadcast(f"{name} has joined the chatroom!")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode().strip()
            if message:
                broadcast(f"{name}: {message}")
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