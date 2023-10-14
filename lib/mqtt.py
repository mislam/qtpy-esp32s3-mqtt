import os
import ipaddress
import socketpool
import wifi

import adafruit_minimqtt.adafruit_minimqtt as minimqtt
from led import *


class _MQTT:
    def __init__(self) -> None:
        self._config = {
            "WIFI_SSID": os.getenv("CIRCUITPY_WIFI_SSID"),
            "WIFI_PASSWORD": os.getenv("CIRCUITPY_WIFI_PASSWORD"),
            "MQTT_BROKER": os.getenv("MQTT_BROKER"),
            "MQTT_PORT": os.getenv("MQTT_PORT"),
            "MQTT_USER": os.getenv("MQTT_USER"),
            "MQTT_PASSWORD": os.getenv("MQTT_PASSWORD"),
            "MQTT_TOPIC": os.getenv("MQTT_TOPIC"),
        }

        self._RECONNECT_INTERVAL: int = 5  # seconds to wait until next attempt
        self._pool: socketpool.SocketPool = None
        self._client: minimqtt.MQTT = None
        self._subscribed = False

    def connect(self):
        self._connect_wifi()
        self._connect_mqtt()

    def _connect_wifi(self):
        """
        Attempt to connect to Wi-Fi, and retry if fails.
        """
        self._pool = socketpool.SocketPool(wifi.radio)
        broker_ip = None
        print("Connecting to Wi-Fi network ", end="")
        stamp = time.monotonic() - self._RECONNECT_INTERVAL

        while broker_ip is None or wifi.radio.ping(broker_ip, timeout=0.3) is None:
            led.blink(BLUE)
            if time.monotonic() - stamp > self._RECONNECT_INTERVAL:
                stamp = time.monotonic()
                print(".", end="")  # Each dot represents an attempt
                # Attempt to connect to Wi-Fi network
                try:
                    wifi.radio.connect(
                        self._config["WIFI_SSID"],
                        self._config["WIFI_PASSWORD"],
                    )
                    broker_ip = ipaddress.ip_address(
                        self._pool.getaddrinfo(self._config["MQTT_BROKER"], 0)[0][4][0]
                    )
                except Exception:
                    pass

        print(" Connected ✔")

    def _connect_mqtt(self):
        # Initialize a minimqtt client
        self._client = minimqtt.MQTT(
            broker=self._config["MQTT_BROKER"],
            port=self._config["MQTT_PORT"],
            username=self._config["MQTT_USER"],
            password=self._config["MQTT_PASSWORD"],
            socket_pool=self._pool,
            keep_alive=10,
            connect_retries=1,
        )

        # Set callback methods
        self._client.on_connect = self.on_connect
        self._client.on_disconnect = self.on_disconnect
        self._client.on_message = self.on_message

        print("Connecting to MQTT broker ", end="")
        stamp = time.monotonic() - self._RECONNECT_INTERVAL

        while not self._client.is_connected():
            led.blink(PURPLE)
            if time.monotonic() - stamp > self._RECONNECT_INTERVAL:
                stamp = time.monotonic()
                print(".", end="")  # Each dot represents an attempt
                # Attempt to connect to MQTT broker
                try:
                    self._client.connect()
                except Exception:
                    pass

    def on_connect(self, client, userdata, flags, rc):
        # This function will be called when the client is connected
        # successfully to the broker.
        led.on(GREEN, wait=1)
        print(" Connected ✔")
        # Subscribe to all changes on the topic.
        if not self._subscribed:
            client.subscribe(self._config["MQTT_TOPIC"] + "/#")
            self._subscribed = True

    def on_disconnect(self, client, userdata, rc):
        # This method is called when the client is disconnected
        print("Disconnected from MQTT Broker!")

    def on_message(self, client, topic, message):
        # This method callled when a client's subscribed feed has a new
        print(f"New message on topic {topic}: {message}")

    def loop(self):
        self._client.loop()


# Instantiate the singleton
mqtt = _MQTT()
