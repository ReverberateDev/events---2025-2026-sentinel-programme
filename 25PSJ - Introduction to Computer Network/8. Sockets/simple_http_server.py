import socket

def handle_request(client_socket):
    request = client_socket.recv(1024).decode()
    
    path = "/"
    if request.startswith("GET"):
        parts = request.split()
        if len(parts) > 1:
            path = parts[1]

    if path == "/":
        response = ("HTTP/1.1 200 OK\r\n"
                   "Content-Type: text/html\r\n\r\n"
                   "<html><body><h1>Welcome to my simple HTTP server!</h1></body></html>")
    else:
        response = ("HTTP/1.1 404 Not Found\r\n"
                   "Content-Type: text/html\r\n\r\n"
                   "<html><body><h1>404 Not Found</h1></body></html>")
    
    client_socket.send(response.encode())

def start_server():
    HOST = 'localhost'
    PORT = 5000
    with socket.socket() as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print(f"Server running on http://localhost:{PORT}")

        try:
            while True:
                conn, addr = sock.accept()
                print(f"Connection from {addr}")
                with conn:
                    handle_request(conn)
        except KeyboardInterrupt:
            print("Shutting down the server.")

if __name__ == "__main__":
    start_server()