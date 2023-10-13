# MQTT Client for Adafruit QT Py ESP32-S3

This repository demonstrates the implementation of an MQTT client on the Adafruit QT Py ESP32-S3 board using CircuitPython. The project showcases how to connect to Wi-Fi, establish a connection to an MQTT broker (specifically Mosquitto running on a Raspberry Pi), subscribe to an MQTT topic, and process incoming messages.

<p align="left">
  <a href="https://fosskey.com">
    <img alt="Fosskey" src="https://github.com/mislam/qtpy-esp32s3-mqtt-client/assets/508043/91db3172-4666-44bf-8af8-faf52b40ada8" width="830" />
  </a>
</p>

## Overview

- **Hardware:** [Adafruit QT Py ESP32-S3](https://learn.adafruit.com/adafruit-qt-py-esp32-s3) \w 4MB Flash and 2MB PSRAM.
- **Platform:** [CircuitPython 8.2.6](https://learn.adafruit.com/adafruit-qt-py-esp32-s3/circuitpython-2)
- **Library:** [Adafruit CircuitPython MiniMQTT v7.4.2](https://github.com/adafruit/Adafruit_CircuitPython_MiniMQTT)

## Features

- **Wi-Fi Connectivity:** The project allows the ESP32-S3 to connect to a Wi-Fi network using credentials from a `settings.toml` file. It handles reconnections in case of signal loss.

- **MQTT Communication:** It establishes a reliable connection to an MQTT broker, utilizing configuration from the `settings.toml` file. It also includes robust mechanisms for automatically re-establishing communication in case of interruptions or losses to the broker.

- **Subscribing to MQTT:** The client subscribes to an MQTT topic. When a message is received on that topic, it is printed to the console.

## Getting Started

To run this project, follow these steps:

1. **Setup CircuitPython:** Ensure that CircuitPython is installed on your Adafruit QT Py ESP32-S3 board.

2. **Configuration:** Modify the `settings.toml` file with your Wi-Fi credentials and MQTT broker details.

3. **Upload Code:** Upload the project code to your board. You can use a tool like [CircuitPython Code Editor](https://code.circuitpython.org/) to transfer files to the board over WiFi.

4. **Execute:** Run the code on your board. It will establish connections to Wi-Fi and MQTT and begin handling MQTT messages.

## Error Handling

The project includes error-handling logic to address situations where the Wi-Fi signal may be lost or the connection to the MQTT broker is disconnected. It attempts to handle these scenarios gracefully.

## Contributing

Contributions to this project are welcome. If you would like to enhance or extend the functionality, please submit issues or pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
