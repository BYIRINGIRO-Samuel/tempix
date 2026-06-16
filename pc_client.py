import serial
import serial.tools.list_ports
import time
import paho.mqtt.client as mqtt

# --- Configuration ---
# Serial Port Configuration
# If COM_PORT is None, the script will try to auto-detect the Arduino.
# You can set it manually, e.g., COM_PORT = "COM3" (Windows) or "/dev/ttyACM0" (Linux)
COM_PORT = None
BAUD_RATE = 9600

# MQTT Broker Configuration
MQTT_BROKER = "157.173.101.159" 
MQTT_PORT = 9210
MQTT_TOPIC = "student/sensor/temperature"

# ---------------------------------------------------------
# MQTT Callbacks
# ---------------------------------------------------------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Successfully connected to broker: {MQTT_BROKER}")
    else:
        print(f"[MQTT] Failed to connect, return code {rc}")

def on_disconnect(client, userdata, rc):
    print("[MQTT] Disconnected from broker.")

# ---------------------------------------------------------
# Auto-detect Serial Port
# ---------------------------------------------------------
def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Many Arduinos contain 'Arduino' or 'CH340' in their description
        if "Arduino" in port.description or "CH340" in port.description:
            return port.device
    
    # Fallback to the first available port if we can't specifically identify Arduino
    if ports:
        return ports[0].device
    return None

# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------
def main():
    print("=== PC Monitoring and MQTT Transmission ===")
    
    # 1. Setup MQTT Client (Compatible with paho-mqtt 2.x)
    try:
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "pc_client_publisher", transport="websockets")
    except AttributeError:
        # Fallback for older paho-mqtt 1.x versions
        mqtt_client = mqtt.Client("pc_client_publisher", transport="websockets")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect
    
    print(f"Connecting to MQTT Broker {MQTT_BROKER}:{MQTT_PORT}...")
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start() # Start network loop in background
    except Exception as e:
        print(f"[ERROR] Could not connect to MQTT Broker: {e}")
        return

    # 2. Setup Serial Connection
    port_to_use = COM_PORT
    if port_to_use is None:
        port_to_use = find_arduino_port()
        
    if port_to_use is None:
        print("[ERROR] No serial ports found. Please connect your Arduino Uno.")
        mqtt_client.loop_stop()
        return
        
    print(f"Connecting to Arduino on Serial Port: {port_to_use} at {BAUD_RATE} baud...")
    
    try:
        ser = serial.Serial(port_to_use, BAUD_RATE, timeout=2)
        time.sleep(2) # Wait for Arduino to reset after serial connection
        print("[Serial] Successfully connected to Arduino.")
    except Exception as e:
        print(f"[ERROR] Could not open Serial port {port_to_use}: {e}")
        mqtt_client.loop_stop()
        return

    # 3. Read Loop
    print("\n--- Starting Real-Time Monitoring ---")
    print(f"Publishing to MQTT Topic: {MQTT_TOPIC}")
    print("Press Ctrl+C to stop.\n")
    
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                
                # Check if it's our temperature data format (TEMP:25.50)
                if line.startswith("TEMP:"):
                    temp_value = line.split(":")[1]
                    
                    # Display in real time
                    print(f"[{time.strftime('%H:%M:%S')}] Received Temperature: {temp_value} °C")
                    
                    # Publish to MQTT Broker
                    mqtt_client.publish(MQTT_TOPIC, temp_value)
                    
                else:
                    # Print other debug info sent from Arduino
                    if line:
                        print(f"[Arduino Debug]: {line}")
                        
            time.sleep(0.1) # Small delay to prevent high CPU usage
            
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
    finally:
        ser.close()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("Disconnected. Goodbye!")

if __name__ == "__main__":
    main()
