import socket
import logging
import traceback
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

weather_data = {
    "London": {"temperature": 18, "humidity": 60, "description": "Partly cloudy"},
    "Paris": {"temperature": 22, "humidity": 55, "description": "Sunny"},
    "New York": {"temperature": 20, "humidity": 70, "description": "Cloudy"},
    "Tokyo": {"temperature": 25, "humidity": 80, "description": "Rainy"}
}

HOST = 'localhost'
PORT = 4000

def handle_client(client_socket):
    while True:
        request_raw = client_socket.recv(1024)
        if not request_raw:
            break
        request = json.loads(request_raw.decode())
            
        if request.get("request") == "weather":
            city = request.get("city", "")
            if city in weather_data:
                info = weather_data[city]
                response = {
                    "result": "success",
                    "city": city,
                    "temperature": info["temperature"],
                    "humidity": info["humidity"],
                    "description": info["description"],
                }
            else:
                response = {"result": "unknown_city", "city": city}
        elif request.get("request") == "get_cities":
            response = {"response": "success", "cities": list(weather_data.keys())}
        else:
            response = {"result": "unsupported_request"}
        response_raw = json.dumps(response).encode()
        client_socket.sendall(response_raw)
    client_socket.close()       

def start_server():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    logging.info(f"Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connected to client: {address}")
        try:
            handle_client(client_socket)
        except Exception as e:
            logging.error("Error handling request: %s", e)
            logging.error(traceback.format_exc())
    
if __name__ == '__main__':
    start_server()
