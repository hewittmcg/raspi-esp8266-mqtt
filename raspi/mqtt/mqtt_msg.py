''' MQTT message handling functions '''

import paho.mqtt.client as mqtt
import csv 
import json
from datetime import datetime
import sqlite3
import os

from app_db import add_node, add_packet

from app import NODE_DB_FILEPATH

# Create config filepath
dirname = os.path.dirname(__file__)
CONFIG_FILEPATH = os.path.join(dirname, "config.json")

DEVICE_JOIN_TOPIC = "join/"
DEVICE_RX_TOPIC = "rx/"

def respond_to_join(client, userdata, msg):
    ''' On join, provision device with new unique hex ID and add device to DB '''
    with open(CONFIG_FILEPATH, 'r') as file:
        config = json.load(file)
        device_id = hex(config["CUR_JOIN_DEVICE_ID"])[2:]
        config["CUR_JOIN_DEVICE_ID"] += 1

    with open(CONFIG_FILEPATH, 'w') as file:
        json.dump(config, file)

    # Append leading zeros to value
    for i in range(0, 4 - len(device_id)):
        device_id = "0" + device_id

    # Send to device
    print("Sending device id " + device_id + " to device")
    client.publish(DEVICE_RX_TOPIC + DEVICE_JOIN_TOPIC, device_id)

    # Register device in DB
    conn = sqlite3.connect(NODE_DB_FILEPATH)
    add_node(conn, device_id, "", str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.close()


def log_msg(client, userdata, msg):
    ''' Log message data under device-specific csv file and to DB '''
    device_id = (str)(msg.topic[-4:])
    print("device id: " + device_id)

    data = msg.payload.decode('utf-8')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("./log/" + device_id + ".csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([time, msg.payload.decode('utf-8')])

    # Write to DB
    conn = sqlite3.connect(NODE_DB_FILEPATH)
    add_packet(conn, data, time, device_id)
    conn.close()
