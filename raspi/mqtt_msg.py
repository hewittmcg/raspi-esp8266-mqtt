''' MQTT message handling functions '''

import paho.mqtt.client as mqtt
import csv 
import json
from datetime import datetime
import sqlite3

from app_db import add_node, add_packet

from app import NODE_DB_FILEPATH

DEVICE_JOIN_TOPIC = "join/"
DEVICE_RX_TOPIC = "rx/"

def respond_to_join(client, userdata, msg):
    ''' On join, provision device with new unique hex ID and add device to DB '''
    print("in respond_to_join call")
    with open("config.json", 'r') as file:
        print("with open")
        config = json.load(file)
        device_id = hex(config["CUR_JOIN_DEVICE_ID"])[2:]
        print("before inc settings device id")
        config["CUR_JOIN_DEVICE_ID"] += 1

    print("before writing to json")
    with open("config.json", 'w') as file:
        json.dump(config, file)

    print("after writing to json")
    # Append leading zeros to value
    for i in range(0, 4 - len(device_id)):
        device_id = "0" + device_id

    # Send to device
    print("Sending device id " + device_id + " to device")
    client.publish(DEVICE_RX_TOPIC + DEVICE_JOIN_TOPIC, device_id)

    # Register device in DB
    conn = sqlite3.connect(NODE_DB_FILEPATH)
    add_node(conn, device_id, "", str(datetime.now().strftime("%H:%M:%S")))
    conn.close()


def log_msg(client, userdata, msg):
    ''' Log message data under device-specific csv file and to DB '''
    device_id = (str)(msg.topic[-4:])
    print("device id: " + device_id)

    data = msg.payload.decode('utf-8')
    time = datetime.now().strftime("%H:%M:%S")

    with open("./log/" + device_id + ".csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%H:%M:%S"), msg.payload.decode('utf-8')])

    # Write to DB
    conn = sqlite3.connect(NODE_DB_FILEPATH)
    add_packet(conn, data, time, device_id)
    conn.close()
