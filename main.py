import supervisor
import time

from mqtt import *


def on_hello(message):
    # Callback for `hello` subtopic
    # when a payload is published at at `my/mqtt/topic/hello`
    print("hello " + message)


def on_welcome(message):
    # Callback for `welcome` subtopic
    # when a payload is published at at `my/mqtt/topic/welcome`
    print("welcome " + message)


# Connect to MQTT broker
mqtt.connect()

# Register callbacks for two subtopics
mqtt.on("hello", on_hello)
mqtt.on("welcome", on_welcome)

# Start a blocking message loop
# NOTE: NO code below this loop will execute
# NOTE: Network reconnection is handled within this loop
while True:
    try:
        mqtt.loop()
    except Exception as e:
        led.on(RED, wait=1)
        print("Error:", e, "\nSystem will soft reboot now.")
        supervisor.reload()
    time.sleep(1)
