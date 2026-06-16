# Embedded Systems Temperature Display and MQTT Monitoring

This project implements a simple embedded system that reads temperature data from an Arduino Uno, displays it on an LCD alongside the candidate's name (with horizontal scrolling if the name is long), and sends the data over USB Serial to a PC. A Python script on the PC reads the serial data and publishes it to an MQTT Broker on a VPS, while displaying it in real-time.

## Project Structure

- `arduino_temp_lcd/arduino_temp_lcd.ino`: The Arduino firmware (C++).
- `pc_client.py`: The Python script running on the PC.
- `architecture_diagram.md`: System architecture diagram.
- `README.md`: This file.

## Requirements

### Hardware
- Arduino Uno
- DHT11 Temperature Sensor (or DHT22)
- 16x2 LCD Display (Standard or I2C. The code currently uses parallel pins 12, 11, 5, 4, 3, 6)
- Jumper wires and Breadboard

### Software
- Arduino IDE (to upload the `.ino` file)
- Python 3.x
- Python packages: `pyserial`, `paho-mqtt`

## Setup Instructions

### 1. Arduino Setup
1. Open `arduino_temp_lcd/arduino_temp_lcd.ino` in the Arduino IDE.
2. Update the `candidateName` variable at the top of the file with your name.
3. Wire your DHT sensor to digital pin `2` (or change the `DHTPIN` define).
4. Wire your LCD according to the pin definitions: `LiquidCrystal lcd(12, 11, 5, 4, 3, 6);`.
5. Upload the code to your Arduino Uno.

### 2. PC Setup
1. Open a terminal/command prompt.
2. Install the required Python dependencies:
   ```bash
   pip install pyserial paho-mqtt
   ```
3. Open `pc_client.py` and ensure the `MQTT_BROKER` address and `MQTT_TOPIC` are set according to your VPS details. 
4. The script auto-detects the Arduino serial port, but you can hardcode it in the `COM_PORT` variable if necessary (e.g., `"COM3"`).

### 3. Execution
1. Ensure the Arduino is plugged into your PC via USB.
2. Run the Python script:
   ```bash
   python pc_client.py
   ```
3. The script will connect to the MQTT broker, connect to the Arduino over Serial, and start printing/publishing the temperature readings in real-time.
4. Verify the published data on your dashboard or by subscribing to the topic using an MQTT client (like MQTTX or mosquitto_sub).

## Communication Names
- **Serial Communication**: UART via USB connection (9600 baud rate).
- **MQTT Topic**: `student/sensor/temperature` (configured in `pc_client.py`).
