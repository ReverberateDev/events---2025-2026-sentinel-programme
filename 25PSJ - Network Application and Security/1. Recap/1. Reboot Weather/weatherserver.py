import socket

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
    client_socket.send(b"Welcome to Weather server!\n")
    
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
    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connected to client: {address}")
        handle_client(client_socket)

if __name__ == '__main__':
    start_server()
