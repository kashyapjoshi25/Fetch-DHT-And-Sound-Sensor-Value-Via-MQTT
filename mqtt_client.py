import paho.mqtt.client as mqtt
import os
import sqlite3
import json

# MQTT Broker Configuration
CUSTOM_MQTT_BROKER = "localhost"  # Use the same MQTT broker configuration as in your sensor code
CUSTOM_MQTT_PORT = 1883

# Function to create the SQLite database and 'sensor_data' table if they don't exist
def initialize_database():
    if not os.path.isfile('dbSensor.db'):
        conn = sqlite3.connect('dbSensor.db')
        conn.close()

    conn = sqlite3.connect('dbSensor.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_type TEXT,
            value REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn, cursor

# Function to insert data into the database
def insert_data(conn, cursor, sensor_type, value):
    try:
#        print(sensor_type)
#        print(value)
        cursor.execute('''
            INSERT INTO sensor_data (sensor_type, value)
            VALUES (?, ?)
        ''', (sensor_type, value))
        conn.commit()
    except sqlite3.Error as db_error:
        print(f"SQLite Error: {db_error}")
    except Exception as other_error:
        print(f"An unexpected error occurred: {other_error}")

def on_message(client, userdata, message):
    try:
        conn, cursor = initialize_database()
        payload = json.loads(message.payload.decode("utf-8"))

        if message.topic == "custom/sensors/all":
 #           print(payload["data"]["temperature"])
 #           print(payload["sound"])
            # Handling data from all sensors
 #           if payload["data"]["temperature"] in payload:
            insert_data(conn, cursor, "temperature", payload["data"]["temperature"])
 #           if payload["data"]["sound"] in payload:
            insert_data(conn, cursor, "sound", payload["data"]["sound"])
 #           if payload["data"]["humidity"] in payload:
            insert_data(conn, cursor, "humidity", payload["data"]["humidity"])
        else:
            # Handling data from individual sensors
            sensor_type = message.topic.split("/")[-1]
            insert_data(conn, cursor, sensor_type, payload["data"])

        print(f"Topic {message.topic}: {payload}")
    except Exception as e:
        print(f"Error processing message: {str(e)}")

print("Select topics to subscribe (separate choices by commas):")
print("1. Temperature")
print("2. Humidity")
print("3. Sound")
print("4. Combined Data")
choices = input("Enter the numbers of your choices (e.g., 1,2,3): ").split(",")

topics = {
    "1": "custom/sensors/temperature",
    "2": "custom/sensors/humidity",
    "3": "custom/sensors/sound",
    "4": "custom/sensors/all",
}

selected_topics = [topics[choice] for choice in choices if choice in topics]

if not selected_topics:
    print("No valid choices selected. Exiting.")
else:
    # MQTT client setup
    custom_client = mqtt.Client()
    custom_client.on_message = on_message

    try:
        custom_client.connect(CUSTOM_MQTT_BROKER, CUSTOM_MQTT_PORT, 60)
        for topic in selected_topics:
            custom_client.subscribe(topic)
        custom_client.loop_forever()
    except Exception as e:
        print(f"Error in MQTT client: {str(e)}")
