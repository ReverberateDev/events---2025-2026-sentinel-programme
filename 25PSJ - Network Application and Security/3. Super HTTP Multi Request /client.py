import socket

HOST = "127.0.0.1"
PORT = 8005

def read_whatever(client_socket, timeout=0.2):
    client_socket.settimeout(timeout)
    chunks = []
    try:
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
    except socket.timeout:
        pass
    return b"".join(chunks)

def send_get_request(client_socket, path="/"):
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {HOST}\r\n"
        f"Connection: keep-alive\r\n"
        f"\r\n"
    )
    client_socket.sendall(request.encode())
    resp = read_whatever(client_socket)
    print(resp.decode("latin-1", errors="replace"))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
send_get_request(client_socket, "/abcd")
send_get_request(client_socket, "/abcd")
client_socket.close()