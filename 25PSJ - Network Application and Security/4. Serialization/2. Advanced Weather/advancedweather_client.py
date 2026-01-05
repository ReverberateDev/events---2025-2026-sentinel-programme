import socket
import json

HOST = 'localhost'
PORT = 4000

def get_weather_info():
    minimum_temperature = int(input("Enter minimum temperature: "))

    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))

    # Getting list of cities
    request = {
        "request": "get_cities"
    }
    request_raw = json.dumps(request).encode()
    client_socket.sendall(request_raw)

    response_raw = client_socket.recv(1024)
    response = json.loads(response_raw.decode())
    cities = response.get("cities", [])

    for city in cities:
        request = {
            "request": "weather",
            "city": city
        }
        request_raw = json.dumps(request).encode()
        client_socket.sendall(request_raw)

        response_raw = client_socket.recv(1024)
        response = json.loads(response_raw.decode())

        if response.get("result") == "success" and response.get("temperature", 0) >= minimum_temperature:
            print(f"== Weather information for {response['city']} ==")
            print(f"Temperature: {response['temperature']}°C")
            print(f"Humidity: {response['humidity']}%")
            print(f"Description: {response['description']}\n")
    
    client_socket.close()

if __name__ == '__main__':
    get_weather_info()
