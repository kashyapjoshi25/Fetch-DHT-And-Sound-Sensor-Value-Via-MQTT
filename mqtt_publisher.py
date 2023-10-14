import Adafruit_DHT
import paho.mqtt.client as mqtt
import json
import time
import RPi.GPIO as GPIO
from datetime import datetime

# Set the GPIO pins for the sensors
temp_sensor_pin = 4  # Replace with the appropriate GPIO pin for temperature
hum_sensor_pin = 4  # Replace with the appropriate GPIO pin for humidity
sound_sensor_pin = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(sound_sensor_pin, GPIO.IN)

# Define the sensor type (DHT11)
sensor_type = Adafruit_DHT.DHT11

# MQTT Broker Configuration
mqtt_broker = "localhost"  # Use localhost if MQTT broker is on the same machine
mqtt_port = 1883
temperature_topic = "custom/sensors/temperature"
sound_topic = "custom/sensors/sound"
humidity_topic = "custom/sensors/humidity"
sensor_topic = "custom/sensors/all"

# Create an MQTT client
def create_mqtt_client():
    client = mqtt.Client()
    client.connect(mqtt_broker, mqtt_port, 60)
    return client

# Publish sensor data
def publish_sensor_data(topic, sensor_type, data):
    client = create_mqtt_client()

    try:
        if data:
            data_with_sensor_type = {
                "sensor_type": sensor_type,
                "data": data,
            }
            client.publish(
                topic,
                payload=json.dumps(data_with_sensor_type),
                qos=0,
                retain=False,
            )
            print(f"Data for {topic} published successfully: {data_with_sensor_type}")
        else:
            print(f"Failed to read data for {topic}.")
    except Exception as e:
        print(f"Error publishing data for {topic}: {str(e)}")
    finally:
        client.disconnect()

# Read temperature data
def read_temp_data():
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor_type, temp_sensor_pin)
        if temperature is not None:
            print(f"Temperature: {temperature:.1f} C")
            return f"{temperature:.1f} C"  # Return only the temperature value
        else:
            print("Failed to read temperature from the sensor.")
            return None
    except Exception as e:
        print(f"Error reading temperature data: {str(e)}")
        return None

# Read humidity data
def read_hum_data():
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor_type, hum_sensor_pin)
        if humidity is not None:
            print(f"Humidity: {humidity:.1f}%")
            return f"{humidity:.1f}%"  # Return only the humidity value
        else:
            print("Failed to read humidity from the sensor.")
            return None
    except Exception as e:
        print(f"Error reading humidity data: {str(e)}")
        return None

# Read sound sensor data
def read_sound_data():
    try:
        sensor_value = GPIO.input(sound_sensor_pin)
        sound_level = 1 if sensor_value == GPIO.HIGH else 0
        print(f"Sound Level: {sound_level}")
        return sound_level  # Return only the sound level
    except Exception as e:
        print(f"Error reading sound data: {str(e)}")
        return None

# Publish combined sensor data
def publish_combined_sensor_data():
    temperature_data = read_temp_data()
    sound_data = read_sound_data()
    humidity_data = read_hum_data()

    if temperature_data and sound_data and humidity_data:
        combined_data = {
            "temperature": temperature_data,
            "sound": sound_data,
            "humidity": humidity_data,
        }
        publish_sensor_data(sensor_topic, "combined", combined_data)

if __name__ == "__main__":
    while True:
        temperature_data = read_temp_data()
        if temperature_data:
            publish_sensor_data(temperature_topic, "temperature", temperature_data)

        sound_data = read_sound_data()
        if sound_data:
            publish_sensor_data(sound_topic, "sound", sound_data)

        humidity_data = read_hum_data()
        if humidity_data:
            publish_sensor_data(humidity_topic, "humidity", humidity_data)

        publish_combined_sensor_data()

        time.sleep(1)
