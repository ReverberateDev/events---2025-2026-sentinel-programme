import socket
import logging
import traceback
import json
import os
import sqlite3  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initial implementation uses an in-memory dictionary.
# This dictionary can be removed once weather data is loaded from JSON files instead.
weather_data = {
    "london": {"temperature": 18, "humidity": 60, "description": "Partly cloudy"},
    "paris": {"temperature": 22, "humidity": 55, "description": "Sunny"},
    "new york": {"temperature": 20, "humidity": 70, "description": "Cloudy"},
    "tokyo": {"temperature": 25, "humidity": 80, "description": "Rainy"}
}

HOST = 'localhost'
PORT = 4000
DB_PATH = os.path.join(os.path.dirname(__file__), "database.sqlite")

def format_weather_info(weather_info):
    return f"Temperature: {weather_info['temperature']} degree Celsius\nHumidity: {weather_info['humidity']}%\nDescription: {weather_info['description']}"

def load_city_weather(city):
    connection = sqlite3.connect(DB_PATH)
    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT temperature, humidity, description FROM cities WHERE city = ?",
            (city.lower(),),
        )
        row = cursor.fetchone()
        if not row:
            return None
        else:
            return {
                "temperature": row[0],
                "humidity": row[1],
                "description": row[2],
            }
    finally:
        connection.close()

def handle_client(client_socket):
    city = client_socket.recv(20).decode().strip().lower()
    if not city:
        # Client disconnected
        return
    
    # Instead of using the in-memory weather_data dictionary,
    # load the weather information from a JSON file that matches the requested city.
    # (e.g., "<city>.json") and return the data from that file.
    weather_info = load_city_weather(city)
    if weather_info:
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

    while True:
        client_socket, address = server_socket.accept()
        logging.info(f"Connected to client: {address}")
        try:
            handle_client(client_socket)
        except Exception as e:
            logging.error("Error handling request: %s", e)
            logging.error(traceback.format_exc())
    
if __name__ == '__main__':
    start_server()
