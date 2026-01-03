import socket

HOST = 'localhost'
PORT = 4000

def get_weather_info():
    city = input("Enter the name of a city: ")
    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))
    welcome = client_socket.recv(1024).decode()
    client_socket.send(city.encode())
    response = client_socket.recv(1024).decode()
    client_socket.close()
    return response

if __name__ == '__main__':
    weather_info = get_weather_info()
    print(weather_info)
