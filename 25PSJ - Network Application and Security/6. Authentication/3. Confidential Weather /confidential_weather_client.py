import socket
import json
import hashlib

HOST = 'localhost'
PORT = 4000

def format_weather_info(weather_info):
    output = ''
    if weather_info['result'] == 'success':
        output = f"== Weather information for {weather_info['city']} ==\n"
        output += f"Temperature: {weather_info['temperature']}°C\nHumidity: {weather_info['humidity']}%\nDescription: {weather_info['description']}"
    elif weather_info['result'] == 'unknown_city':
        output = f"** Server has no data on {weather_info['city']} **"
    else:
        output = "** Error retrieving weather information **"
    return output

def get_weather_info():
    username = input("Enter username: ")
    password = input("Enter password: ")
    city = input("Enter the name of a city: ")

    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))

    client_socket.send(json.dumps({"request": "auth", "username": username}).encode())

    resp1 = json.loads(client_socket.recv(1024).decode())
    challenge = resp1["challenge"]

    digest = hashlib.sha256((challenge + password).encode()).hexdigest()
    client_socket.send(json.dumps({"request": "auth_response", "response": digest}).encode())

    client_socket.send(json.dumps({"request": "weather", "city": city}).encode())

    response = json.loads(client_socket.recv(1024).decode())
    print(format_weather_info(response))
    client_socket.close()

if __name__ == '__main__':
    get_weather_info()
