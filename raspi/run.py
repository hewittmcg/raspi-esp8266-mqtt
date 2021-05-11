''' Run app + MQTT packet handler modules using multithreading '''

import sys
import threading

# Add app and mqtt folders to PATH
sys.path.append("./app")
sys.path.append("./mqtt")

# These need to be after adding to the PATH, so exclude from formatting
from mqtt_main import start as mqtt_start  # nopep8
from app import run as run_app  # nopep8

if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=mqtt_start)

    # App needs to be run with debug=False to work with multithreading
    app_thread = threading.Thread(target=run_app, args=(False,))

    mqtt_thread.start()
    app_thread.start()
