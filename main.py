import supervisor
import time

from mqtt import *

mqtt.connect()

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
