# raspi-esp8266-mqtt

The general idea behind this is to create a simple way to track sensor readings (e.g. water level in plant pots) from devices connected to the same network, creating a simple smart home framework.  

[ESP8266](https://www.espressif.com/en/products/socs/esp8266)-based microcontrollers are used as the devices. A Raspberry Pi 4 Model B is used to aggregate device reports sent over MQTT.  It also sends a unique device ID to devices when they are first powered on.  This ID is stored in RTC memory so that devices don't need to rejoin each time new firmware is loaded.  A Flask app with a Vue frontend is hosted on the Pi, through which devices and their respective messages can be viewed.

## Getting Started

### Raspberry Pi
SSH into the Pi.  Note its local IP, as this will be needed when setting up devices.

Make sure everything is up to date (optional)
```bash
sudo apt-get update
sudo apt-get upgrade
```
Clone repo and install required packages
```bash
sudo apt-get install mosquitto
git clone https://github.com/hewittmcg/raspi-esp8266-mqtt.git
cd raspi-esp8266-mqtt/raspi
pip install -r requirements.txt
cd client
sudo npm install
cd ..
```

Mosquitto defaults to listen to port 1883, but this software is configured to use port 2000 instead.

You can either: 
- Change the port mosquitto listens to by editing the `Mosquitto.conf` file in /etc/mosquitto and adding the line `listener 2000` or
- Change the `PORT` field in raspi/mqtt/config.json to 1883.  Note that in this case you will also have to change the `mqttPort` var in any ESP8266 files to 1883 prior to flashing.

Now, run the software:
```bash
sudo python run.py
```

In a separate terminal, set up the frontend:
```bash
cd client
sudo npm run serve
```

Navitage to the port 8080 at the IP of the Pi and you should see a webpage titled "Devices".

### ESP8266
*This section assumes you have a general understanding of how to setup the Arduino IDE to work with an ESP8266.  If not, [this article](https://randomnerdtutorials.com/how-to-install-esp8266-board-arduino-ide/) offers a good explanation.*

Clone the repo to your PC.

Open the Arduino IDE and install the [PubSubClient](https://www.arduino.cc/reference/en/libraries/pubsubclient/) library.

Open `serial_demo.ino` (esp8266/serial_demo).  Change `ssid` and `pass` to your WiFi SSID and password respectively.  Change `mqttServer` to the IP of the Pi.  If you are using a port other than 2000 to send MQTT messages, change `mqttPort` to this port now.

**WARNING: ESP8266 MCUs only work on 2.4 GHz WiFi bands**

Open the serial monitor and upload the firmware to your ESP8266.  You should see output similar to this:

```
Connecting to WiFi...
Connected to WiFi
Connecting to MQTT.
Connected to MQTT Broker
Device has not joined network, joining
Join complete
Enter value to broadcast over MQTT
```

At this point, refresh the Pi webpage and a device name should appear.  Click on this to view the messages from that device -- currently there should be none.

Send a string to the ESP8266 over serial **with newlines enabled**.  Refresh the web page; this message should now be shown, along with the time it arrived.

