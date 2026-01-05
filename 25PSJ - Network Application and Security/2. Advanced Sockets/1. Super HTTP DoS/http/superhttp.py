import socket
import os
import json
import logging
import mimetypes
import traceback
from urllib.parse import unquote_plus

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def handle_request(client_socket):
    # Kill after 10 seconds
    try:
        client_socket.settimeout(10)
        request = client_socket.recv(config['max_request_size']).decode()
    except socket.timeout:
        send_response(client_socket, '408 Request Timeout', '<h1>408 Request Timeout</h1>')
        client_socket.close()
        return
    if not request:
        raise ConnectionResetError()

    headers, body = request.split('\n\n', 1)
    first_line = headers.split('\n')[0]
    method, path, _ = first_line.split()
    path = unquote_plus(path.split('?')[0])

    logging.info("Request: %s %s", method, path)

    # Task 1 & 2
    """
    Add additional GET handlers below for specific paths required in Task 1 & 2.

    Note: Each path should be matched explicitly and routed to its corresponding handler function
    """
    
    if method == 'POST' and path == '/upload':
        handle_upload_userfile(client_socket, body)
    elif method == 'GET':
        if path == '/userfile.txt':
            handle_userfile(client_socket, headers)
        elif path == '/myuseragent':
            handle_myuseragent(client_socket, headers)
        else:
            serve_static_files(client_socket, path)
    else:
        send_response(client_socket, '400 Bad Request', '<h1>400 Bad Request</h1>')

    client_socket.shutdown(socket.SHUT_RDWR)

def serve_static_files(client_socket, path):
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

def handle_upload_userfile(client_socket, body):
    file_path = os.path.join(config['upload_dir'], 'userfile.txt')
    with open(file_path, 'wb') as file:
        file.write(unquote_plus(body).encode())
        send_response(client_socket, '200 OK', '<h1>File uploaded successfully</h1>')

# Task 1 handler function
def handle_userfile(client_socket, headers):
    """
    Handle GET requests to /userfile.txt.

    This handler should return the contents of the file that was previously
    uploaded using the /upload endpoint.

    Requirements:
    - The file is stored in the server's upload directory, inside userfile.txt
    - The response body should contain the file contents as plaintext
    """
    # Insert Code here
    first_line = headers.split('\r\n')[0]
    method, path, _ = first_line.split()
    path = unquote_plus(path.split('?')[0])

    if path == '/userfile.txt':
        file_path = os.path.join(config['upload_dir'], 'userfile.txt')
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
            send_response(client_socket, '200 OK', content)
        else:
            send_response(client_socket, '404 Not Found', '<h1>404 Not Found</h1>')


# Task 2 handler function
def handle_myuseragent(client_socket, headers):
    """
    Handle GET requests to /myuseragent.

    This handler should extract the User-Agent value from the HTTP request
    headers and return it as plaintext.

    Requirements:
    - The User-Agent value must be taken from the request headers
    - Only the header value (not 'User-Agent:') should be returned
    - The response should be in plaintext, not HTML

    Hints:
    - The headers parameter is a single string containing all request headers
    - Individual headers are separated by CRLF ('\\r\\n')
    - The User-Agent header starts with 'User-Agent:'

    Optional:
    - If no User-Agent header is present, return a 400 Bad Request response
    """    
    # Insert Code here
    first_line = headers.split('\r\n')[0]
    method, path, _ = first_line.split()
    path = unquote_plus(path.split('?')[0])
    if path == '/myuseragent':
        user_agent = None
        for header_line in headers.split('\r\n')[1:]:
            if header_line.lower().startswith('user-agent:'):
                user_agent = header_line.split(':', 1)[1].strip()
                break
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
