import socket
import logging
import traceback
import json
import os
import sqlite3  
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HOST = 'localhost'
PORT = 4000
API_KEY = os.environ.get("OWM_API_KEY")

with open("coordinates.json", "r") as file:
    coordinates = json.load(file)

def format_weather_info(weather_info):
    return (
        f"Temperature: {weather_info['temperature']} degree Celsius\n"
        f"Humidity: {weather_info['humidity']}%\n"
        f"Description: {weather_info['description']}"
    )


def load_city_weather(city):
    coordinate = coordinates.get(city)
    if not coordinate:
        return None
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/weather",
        params={
            "lat": coordinate["latitude"],
            "lon": coordinate["longitude"],
            "appid": API_KEY,
            "units": "metric"
        }
    )
    if response.status_code != 200:
        logging.error(f"Failed to fetch weather data: {response.status_code}")
        return None
    data = response.json()
    weather_info = {
        "temperature": round(data["main"]["temp"]),
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"].capitalize(),
    }
    return weather_info


def handle_client(client_socket):
    city = client_socket.recv(20).decode().strip().lower()
    if not city:
        # Client disconnected
        return
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
