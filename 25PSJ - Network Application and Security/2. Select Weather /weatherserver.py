import socket
import select
import logging

logging.basicConfig(level=logging.INFO) 

weather_data = {
    "London": {"temperature": 18, "humidity": 60, "description": "Partly cloudy", "rainfall" : "10"},
    "Paris": {"temperature": 22, "humidity": 55, "description": "Sunny", "rainfall" : "5"},
    "New York": {"temperature": 20, "humidity": 70, "description": "Cloudy", "rainfall" : "15"},
    "Tokyo": {"temperature": 25, "humidity": 80, "description": "Rainy", "rainfall" : "20"},
    "Townsville": {"temperature": 30, "humidity": 50, "description": "Sunny", "rainfall" : "2"}
}

HOST = 'localhost'
PORT = 4000

def format_weather_info(weather_info):
    return f"Temperature: {weather_info['temperature']}°C\nHumidity: {weather_info['humidity']}%\nDescription: {weather_info['description']}\nRainfall (mm): {weather_info['rainfall']}"

def handle_client(client_socket):
    logging.info("Client connected")
    
    city = client_socket.recv(30).decode().strip()
    if not city:
        # Client disconnected
        return
    if city in weather_data:
        weather_info = weather_data[city]
        response = f"Weather information for {city}:\n{format_weather_info(weather_info)}"
    else:
        response = "City not found"
    client_socket.send(response.encode())
    client_socket.close()

def start_server():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    logging.info(f"Server is listening on {HOST}:{PORT}")

    sockets = [server_socket]

    while True:
        read_sockets, _, _ = select.select(sockets, [], [])
        for sock in read_sockets:
            if sock == server_socket:
                client_socket, addr = server_socket.accept()
                logging.info(f"Connection from {addr}")
                sockets.append(client_socket)
            else:
                handle_client(sock)
                sock.send(b"Welcome to Weather server!\n")
                sockets.remove(sock)


if __name__ == '__main__':
    start_server()
