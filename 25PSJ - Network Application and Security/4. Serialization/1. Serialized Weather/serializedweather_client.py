import socket
import json

HOST = 'localhost'
PORT = 4000

def get_weather_info():
    city = input("Enter the name of a city: ")
    request = {
        "request" : "weather",
        "city" : city
    }
    request_raw = json.dumps(request).encode()

    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))
    client_socket.sendall(request_raw)

    response_raw = client_socket.recv(1024)
    response = json.loads(response_raw.decode())

    if response.get("result") == "success":
        print(f"== Weather information for {response['city']} ==")
        print(f"Temperature: {response['temperature']}°C")
        print(f"Humidity: {response['humidity']}%")
        print(f"Description: {response['description']}")
    elif response.get("result") == "unknown_city":
        print(f"** Server has no data on {response.get('city','')} **")
    else:
        print("Unsupported request")
    
    client_socket.close()

if __name__ == '__main__':
    get_weather_info()
