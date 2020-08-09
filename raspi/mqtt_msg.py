# Message handling functions for MQTT/ESP8266

import paho.mqtt.client as mqtt

import csv
from datetime import datetime

# handle join requests, provision device
def respond_to_join(client, userdata, msg):
    print("Unimplemented")
    # TODO: provision device with unique ID to be stored in RTC memory

# Log message data under csv file corresponding to device in question
def log_msg(client, userdata, msg):
    device_id = (str)(msg.topic[-4:])
    print("device id: " + device_id)
    with open("./log/" + device_id + ".csv", "a") as file:
    # with open("./log/testfilename.csv", "a") as file:  
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%H:%M:%S"), msg.payload.decode('utf-8')])