import os
import board
import neopixel
import supervisor
import time
import socketpool
import wifi
import ipaddress
import adafruit_minimqtt.adafruit_minimqtt as minimqtt

# Load MQTT config
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = os.getenv("MQTT_PORT")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

# Neopixel colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

# Initialize the Neopixel LED
led = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3)

# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

def blink(color, freq=0.3):
    led.fill(color)
    time.sleep(0.3)
    led.fill((0,0,0))
    time.sleep(0.3)

def lit(color):
    led.fill(color)
    time.sleep(1)

def wifi_connect():
    print("Connecting to Wi-Fi...", end="")
    MQTT_BROKER_IP = None
    while MQTT_BROKER_IP is None or wifi.radio.ping(MQTT_BROKER_IP) is None:
        blink(BLUE, freq=0.1)
        # Attempt to connect to Wi-Fi
        try:
            wifi.radio.connect(
                os.getenv("CIRCUITPY_WIFI_SSID"),
                os.getenv("CIRCUITPY_WIFI_PASSWORD"),
            )
            MQTT_BROKER_IP = ipaddress.ip_address(pool.getaddrinfo(MQTT_BROKER, 0)[0][4][0])
        except Exception:
            continue
    print("Connected")
    
    
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    lit(GREEN)
    print("Connected")
    # Subscribe to all changes on the topic.
    client.subscribe(MQTT_TOPIC + "/#")

def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from MQTT Broker!")


def message(client, topic, message):
    # This method callled when a client's subscribed feed has a new
    print(f"New message on topic {topic}: {message}")

wifi_connect() # Connect to Wi-Fi

print("Connecting to MQTT broker...", end="")

# Set up a MiniMQTT Client
mqtt = minimqtt.MQTT(
    broker=MQTT_BROKER,
    port=MQTT_PORT,
    username=MQTT_USER,
    password=MQTT_PASSWORD,
    socket_pool=pool,
    keep_alive=10,
    connect_retries=1,
)

# Setup the callback methods above
mqtt.on_connect = connected
mqtt.on_disconnect = disconnected
mqtt.on_message = message

while not mqtt.is_connected():
    blink(PURPLE)
    # Attempt to connect to MQTT broker
    try:
        mqtt.connect()
    except Exception:
        pass

# Start a blocking message loop...
# NOTE: NO code below this loop will execute
# NOTE: Network reconnection is handled within this loop
while True:
    try:
        mqtt.loop()
    except Exception as e:
        lit(RED)
        supervisor.reload()
    time.sleep(1)
