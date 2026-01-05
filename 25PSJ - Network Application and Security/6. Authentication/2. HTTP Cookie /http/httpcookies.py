import socket
import os
import json
import logging
import mimetypes
import traceback
from urllib.parse import unquote_plus
import base64
import random
import string

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ADMIN_USER = "Admin"
ADMIN_PASS = "Password1!"

# Utility functions

def parse_request(request):
    def parse_headers(header_block):
        headers = {}
        for line in header_block.split('\r\n')[1:]:
            if ': ' in line:
                key, value = line.split(': ', 1)
                headers[key.strip().lower()] = value.strip()
        return headers
    
    headers, body = request.split('\r\n\r\n', 1)
    first_line = headers.split('\r\n')[0]
    method, path, _ = first_line.split()
    path = unquote_plus(path.split('?')[0])
    headers = parse_headers(headers)

    return {
        "method": method,
        "path": path,
        "headers": headers,
        "body": body
    }

def load_config():
    default_config = {
        "host": "localhost",
        "port": 8005,
        "static_files_dir": "www",
        "upload_dir": "uploads",
        "max_request_size": 1048576,  # 1 MB
    }
    return default_config

config = load_config()
cookies = set()

def handle_request(client_socket):
    request_raw = client_socket.recv(config['max_request_size']).decode()

    request = parse_request(request_raw)
    if not request:
        raise ConnectionResetError()
    method = request["method"]
    path = request["path"]
    logging.info("Request: %s %s", request["method"], request["path"])
    
    if method == 'POST':
        if request["path"] == '/upload':
            handle_upload_userfile(client_socket, request)
        elif path == '/login':
            handle_login(client_socket, request)
    elif method == 'GET':
        if path == '/userfile.txt':
            handle_userfile(client_socket, request)
        elif path == '/myuseragent':
            handle_myuseragent(client_socket, request)
        elif path == '/secret.html':
            handle_secret(client_socket, request)
        else:
            handle_static_file(client_socket, request)
    else:
        send_response(client_socket, '400 Bad Request', '<h1>400 Bad Request</h1>')

    client_socket.shutdown(socket.SHUT_RDWR)

def handle_static_file(client_socket, request):
    path = request["path"]
    if path == '/':
        path = '/index.html'
    file_path = os.path.join(config['static_files_dir'], path.strip('/'))
    if not os.path.isfile(file_path):
        send_response(client_socket, '404 Not Found', '<h1>404 Not Found</h1>')
        return

    mime_type, _ = mimetypes.guess_type(file_path)
    with open(file_path, 'rb') as file:
        response_body = file.read()
    send_response(client_socket, '200 OK', response_body, mime_type)

def handle_login(client_socket, request):
    body = request["body"]
    decoded = base64.b64decode(body).decode()
    creds = json.loads(decoded)
    if creds.get("username") == ADMIN_USER and creds.get("password") == ADMIN_PASS:
        cookie = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        cookies.add(cookie)
        send_response(client_socket, '200 OK', cookie, 'text/plain')
    else:
        send_response(client_socket, '401 Unauthorized', '<h1>401 Unauthorized</h1>')
    

def handle_secret(client_socket, request):
    cookie = request["headers"].get("client-cookie")
    if cookie is None or cookie not in cookies:
        send_response(client_socket, '403 Forbidden', '<h1>403 Forbidden</h1>')
    else:
        handle_static_file(client_socket, request)

def handle_upload_userfile(client_socket, request):
    file_path = os.path.join(config['upload_dir'], 'userfile.txt')
    with open(file_path, 'wb') as file:
        file.write(unquote_plus(request["body"]).encode())
        send_response(client_socket, '200 OK', '<h1>File uploaded successfully</h1>')

def handle_userfile(client_socket, request):
    path = request["path"]

    if path == '/userfile.txt':
        file_path = os.path.join(config['upload_dir'], 'userfile.txt')
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
            send_response(client_socket, '200 OK', content)
        else:
            send_response(client_socket, '404 Not Found', '<h1>404 Not Found</h1>')

def handle_myuseragent(client_socket, request):
    headers = request["headers"]
    user_agent = headers.get('user-agent')

    if user_agent:
        send_response(client_socket, '200 OK', user_agent)
    else:
        send_response(client_socket, '400 Bad Request', '<h1>400 Bad Request</h1>')


def send_response(client_socket, status, content, content_type='text/html'):
    length = len(content)
    headers = f"Content-Type: {content_type}\r\nContent-Length: {length}"
    response = f"HTTP/1.1 {status}\r\n{headers}\r\n\r\n"

    rsp = response.encode('latin-1')
    rsp += content if isinstance(content, bytes) else content.encode()
    client_socket.sendall(rsp)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((config['host'], config['port']))
    server_socket.listen(5)
    logging.info("Server is running on http://%s:%d", config['host'], config['port'])

    while True:
        try:
            client_socket, _ = server_socket.accept()
            handle_request(client_socket)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error("Error handling request: %s", e)
            logging.error(traceback.format_exc())
        
    server_socket.close()
    logging.info("Server has been stopped.")

if __name__ == '__main__':
    start_server()
