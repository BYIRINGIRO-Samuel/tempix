# System Architecture Diagram

```mermaid
flowchart TD
    %% Hardware Layer
    subgraph Hardware [Arduino Environment]
        Sensor[DHT11/LM35 Temperature Sensor] -->|Analog/Digital Signal| Arduino[Arduino Uno]
        Arduino -->|Parallel/I2C Control| LCD[16x2 LCD Display]
    end

    %% Communication Interface
    Arduino -->|USB Serial Communication| USB[PC Serial Port / USB]

    %% Software Layer
    subgraph Software [PC Environment]
        USB --> Python[PC Python Client Script]
        Python -->|Display| Terminal[Real-time Terminal Display]
    end

    %% Cloud / Network Layer
    Python -->|MQTT Publish via TCP/IP| MQTT[MQTT Broker on VPS]

    %% Network Consumers
    subgraph Consumers [Remote Access]
        MQTT --> Dashboard[Web Dashboard / Node-RED / App]
    end
```

## Communication Protocols Used

As requested by the exam requirements:

1. **Serial Communication between Arduino and PC**: 
   - Protocol: UART over USB
   - Port: e.g., `COM3` (Windows) or `/dev/ttyACM0` (Linux)
   - Baud Rate: 9600 bps

2. **MQTT Topic used for publishing**:
   - Protocol: MQTT (TCP/IP Port 1883)
   - Topic Name: `student/sensor/temperature` (Configurable in `pc_client.py`)
