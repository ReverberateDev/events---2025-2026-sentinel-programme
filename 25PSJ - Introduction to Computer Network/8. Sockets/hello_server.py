import socket

def main():
    with socket.socket() as server_socket:
        server_socket.bind(('localhost', 5000))
        server_socket.listen()
        print("Server is listening on port 5000...")
        
        while True:
            try:
                connection, client_address = server_socket.accept()
                print(f"Connection from {client_address}")
                
                connection.send("Hello".encode())

                connection.close()
                print(f"Connection with {client_address} closed")
                
            except KeyboardInterrupt:
                print("Ending program")
                break

if __name__ == "__main__":
    main()