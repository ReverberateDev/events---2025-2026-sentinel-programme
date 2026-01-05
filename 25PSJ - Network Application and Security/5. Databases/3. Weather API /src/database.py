import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.sqlite")

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        city TEXT PRIMARY KEY,
        temperature INTEGER,
        humidity INTEGER,
        description TEXT
    )
""")

connection.commit()

while True:
    city = input("City: ")
    if city == "-1":
        break
    temperature = input("Temperature: ")
    humidity = input("Humidity: ")
    description = input("Description: ")

    cursor.execute("""
        INSERT INTO cities (city, temperature, humidity, description)
        VALUES (?, ?, ?, ?)
    """, (city, temperature, humidity, description))

    connection.commit()

while True:
    city = input("City to delete: ")
    if city == "-1":
        break
    cursor.execute("""
        DELETE FROM cities WHERE city = ?
    """, (city,))

while True:
    city = input("City to enquire: ")
    if city == "-1":
        break
    cursor.execute("""
        SELECT temperature, humidity, description FROM cities WHERE city = ? 
    """, (city,))

    row = cursor.fetchone()
    print(row)