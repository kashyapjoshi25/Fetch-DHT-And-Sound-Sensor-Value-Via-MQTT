MQTT Sensor Data Publisher and Client
This repository contains Python scripts for publishing sensor data to an MQTT broker and subscribing to sensor data from the MQTT broker using a client.

Publisher (mqtt_publisher.py)
The mqtt_publisher.py script reads data from sensors (temperature, humidity, and sound) and publishes it to an MQTT broker.

Configuration
MQTT Broker Configuration:
You need to specify the MQTT broker details in the script:
mqtt_broker: localhost
mqtt_port: The MQTT broker's port (default is 1883).



MQTT topics:
temperature_topic: Topic for temperature data.
sound_topic: Topic for sound data.
humidity_topic: Topic for humidity data.
sensor_topic: Topic for combined sensor data.


Running the Publisher
To run the publisher, open a terminal and execute the following command:
"python mqtt_publisher.py"
The script will continuously read sensor data and publish it to the MQTT broker.

Client (mqtt_client.py)
The mqtt_client.py script subscribes to MQTT topics and stores received sensor data in a SQLite database.

Configuration
MQTT Broker Configuration:localhost
You need to specify the MQTT broker details in the script:
MQTT_BROKER: The address of your MQTT broker.
MQTT_PORT: The MQTT broker's port (default is 1883).
SQLite Database:
The script will create an SQLite database named dbSensor.db to store sensor data. You don't need to configure this; it will create the database file automatically.
Running the Client
To run the client, open a separate terminal and execute the following command:

"python mqtt_client.py"
The script will prompt you to select which MQTT topics to subscribe to. After choosing the topics, it will listen for data published to those topics and store it in the SQLite database.


Database
The client script uses an SQLite database to store sensor data. The database file (dbSensor.db) is created automatically when the client is run. You can access the data in the database for further analysis or visualization.

Running Publisher and Client
For the complete system to work, open two separate terminals, one for the publisher and another for the client. Run them side by side, and they will communicate via the MQTT broker.

