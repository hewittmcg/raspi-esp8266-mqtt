# Message handling functions for MQTT/ESP8266

import paho.mqtt.client as mqtt

DEVICE_JOIN_TOPIC = "join/"
DEVICE_RX_TOPIC = "rx/"

import csv, json
from datetime import datetime
import time


def respond_to_join(client, userdata, msg):
    ''' On join, provision device with new hex ID to be stored in RTC memory '''
    with open("settings.json", 'r') as file:
        settings = json.load(file)
        device_id = hex(settings["cur_join_device_id"])[2:]
        settings["cur_join_device_id"] += 1
    with open("settings.json", 'w') as file:
        json.dump(settings, file)
    # Append leading zeros to value
    for i in range(0, 4 - len(device_id)):
        device_id = "0" + device_id
    # Send to device
    print("Sending device id " + device_id + "to device")
    client.publish(DEVICE_RX_TOPIC + DEVICE_JOIN_TOPIC, device_id)


def log_msg(client, userdata, msg):
    ''' Log message data under csv file corresponding to device in question '''
    device_id = (str)(msg.topic[-4:])
    print("device id: " + device_id)
    with open("./log/" + device_id + ".csv", "a") as file:
    # with open("./log/testfilename.csv", "a") as file:  
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%H:%M:%S"), msg.payload.decode('utf-8')])