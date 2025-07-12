import socket

def main():
    message = input("Enter your message: ")
    with socket.socket() as sock:
        sock.connect(('localhost', 5000))
        sock.send(message.encode())
        response = sock.recv(1024)
        print("Received from server:", response.decode())

if __name__ == "__main__":
    main()