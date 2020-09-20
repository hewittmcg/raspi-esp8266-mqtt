# Module handling MQTT messages sent by an ESP8266 microcontroller.
# Reqires a mosquitto broker to be set up on the port designated by MQTT_PORT

import paho.mqtt.client as mqtt
from mqtt_msg import respond_to_join, log_msg

import os, json

# Load info from config file
with open("config.json") as file:
    config = json.load(file)

MQTT_PORT = config["PORT"]

# Consts for device topics
DEVICE_JOIN_TOPIC = "join/"
DEVICE_TX_TOPIC = "tx/" 
DEVICE_RX_TOPIC = "rx/"


def on_connect(client, userdata, flags, rc):
    ''' Callback to run on MQTT connection '''
    print('Connected to MQTT Broker')

    # Subscribe to tx message topic
    client.subscribe('#')


def on_message(client, userdata, msg):
    ''' Callback to run on reception of MQTT message '''
    print('msg: ' + str(msg.payload.decode('utf-8')))
    print('topic: ' + msg.topic)
    # Respond to device joining for the first time.
    if msg.topic[-8:] == DEVICE_TX_TOPIC + DEVICE_JOIN_TOPIC:
        print("JOIN REQUEST RECEIVED")
        respond_to_join(client, userdata, msg)
    elif msg.topic[:3] == DEVICE_TX_TOPIC:
        print("NORMAL MSG RECEIVED")
        log_msg(client, userdata, msg)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start():
    ''' Create log file and start listening to MQTT port '''
    if not os.path.exists("./log"):
        os.mkdir("log")
    
    client.connect('localhost', MQTT_PORT)
    client.loop_forever()


if __name__ == "__main__":
    start()

