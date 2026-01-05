import socket
import logging
import traceback
import json
import string
import random
import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

weather_data = {
    "London": {"temperature": 18, "humidity": 60, "description": "Partly cloudy"},
    "Paris": {"temperature": 22, "humidity": 55, "description": "Sunny"},
    "New York": {"temperature": 20, "humidity": 70, "description": "Cloudy"},
    "Tokyo": {"temperature": 25, "humidity": 80, "description": "Rainy"}
}

USERS_DB = [
    {"username": "bob", "password": "b0bsPassIsL1t"},
]

HOST = 'localhost'
PORT = 4000

def handle_client(client_socket):
    def find_user(username):
        for user in USERS_DB:
            if user["username"] == username:
                return user
        return None
    
    def make_challenge(length = 10):
        alphabet = string.ascii_letters + string.digits
        return ''.join(random.choice(alphabet) for _ in range(length))
    
    # Username login
    print("Receiving username...")
    msg = client_socket.recv(1024).decode()
    if not msg:
        # Client disconnected
        return

    request_obj = json.loads(msg)
    
    request = request_obj.get("request")
    if request != "auth":
        client_socket.send(json.dumps({"result" : "unsupported_request"}).encode())
        return
    
    user = find_user(request_obj.get("username"))
    if not user:
        client_socket.send(json.dumps({"result" : "unknown_user"}).encode())
        return
    
    # Challenge
    print("Sending challenge...")
    challenge = make_challenge()
    client_socket.send(json.dumps({"result" : "challenge", "challenge" : challenge}).encode())

    print("Receiving challenge response...")
    # Receive challenge response
    msg = client_socket.recv(1024).decode()
    if not msg:
        # Client disconnected
        return
    
    request_obj = json.loads(msg)

    request = request_obj.get("request")
    if not (request == "auth_response" and "response" in request_obj):
        print("Unsupported request received during auth response")
        client_socket.send(json.dumps({"result" : "unsupported_request"}).encode())
        return

    expected = hashlib.sha256((challenge + user["password"]).encode()).hexdigest()
    if request_obj["response"] != expected:
        print("Auth failed.")
        client_socket.send(json.dumps({"result" : "auth_failed"}).encode())
        return
    
    # Receive weather request
    print("Auth successful. Receiving weather request...")
    msg = client_socket.recv(1024).decode()
    if not msg:
        # Client disconnected
        return
    request_obj = json.loads(msg)
    request = request_obj.get("request")
    if request != "weather":
        client_socket.send(json.dumps({"result" : "unsupported_request"}).encode())
        return
    city = request_obj.get("city").lower().capitalize()
    if city not in weather_data:
        client_socket.send(json.dumps({"result" : "unknown_city", "city" : city}).encode())
        return
    info = weather_data[city]
    response = {
        "result": "success",
        "city": city,
        "temperature": info["temperature"],
        "humidity": info["humidity"],
        "description": info["description"],
    }
    client_socket.send(json.dumps(response).encode())
    client_socket.close()


def start_server():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    logging.info(f"Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        logging.info(f"Connected client: {address}")
        try:
            handle_client(client_socket)
        except Exception as e:
            logging.error("Error handling request: %s", e)
            logging.error(traceback.format_exc())
    

if __name__ == '__main__':
    start_server()
