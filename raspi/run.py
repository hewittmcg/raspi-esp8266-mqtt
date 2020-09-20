''' Run app + handle MQTT packets '''

from app import run as run_app
from mqtt_main import start as mqtt_start

import threading 
import time

if __name__ == "__main__":
    mqtt_thread = threading.thread(target=mqtt_start)
    app_thread = threading.thread(target=run_app)

    mqtt_thread.start()
    app_thread.start()


    
