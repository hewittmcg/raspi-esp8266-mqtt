''' Run app + MQTT packet handler modules using multithreading '''

from app import run as run_app
from mqtt_main import start as mqtt_start

import threading

if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=mqtt_start)

    # App needs to be run with debug=False to work with multithreading
    app_thread = threading.Thread(target=run_app, args=(False,))

    mqtt_thread.start()
    app_thread.start()


    
