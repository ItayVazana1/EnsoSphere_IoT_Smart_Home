
# 🏡 Smart Apartment IoT Simulation - Full Project Summary

This document provides a **comprehensive overview** of the Smart Apartment IoT Simulation System, covering:
- Rooms & characters (inhabitants)
- Seasonal routines
- Key system goals
- Required achievements
- General system flow
- Expanded section on MQTT, including common actions and code blocks

---

## 📍 Rooms Overview

| Room | Description |
|---|---|
| Living Room | Main shared space - central to activity and automation |
| Kitchen | Cooking area with specific devices and sensors |
| Bedroom | Private sleeping area |
| Kids Room | Child’s bedroom |
| Bathroom | Wet area with humidity & ventilation control |
| Balcony | Outdoor space with weather-sensitive devices |
| Entrance | Front door with security and smart lock |
| Hallway | Interior hallway connecting rooms |
| Outdoor (General) | External environmental sensors |
| Entire Home | Whole-house systems (security, central monitoring) |

---

## 👥 Inhabitants (Characters)

| Character | Description |
|---|---|
| Parent 1 | Adult, follows work-home routine |
| Parent 2 | Adult, work-from-home with cooking duties |
| Child | Attends school, plays in Kids Room |
| Pet (Dog/Cat) | Triggers Pet Feeder and interacts with motion sensors |
| Visitors (Guests) | Trigger doorbell, entrance routines, and notifications |

---

## 📆 Seasonal Routines

### 🔹 Winter
- Increased heating system usage (Air Conditioner on heating mode)
- Early sunset triggers evening lighting routines
- Humidity sensors play key role in bathroom ventilation

### 🔹 Summer
- Frequent use of balcony blinds (heat management)
- More open windows for ventilation (Window Actuators)
- Morning light triggers automatic wake-up routines

### 🔹 Spring
- Balanced climate with mixed heating/cooling
- Outdoor sensors detect pollen count or air quality
- More balcony and outdoor activity

### 🔹 Autumn
- Gradual transition routines - cooling in early autumn, heating in late autumn
- More reliance on scheduled routines (less manual overrides)

---

## 🎯 Key Required Achievements

- ✅ Simulated environment with accelerated time & seasonal weather
- ✅ Modular devices & sensors, each with a dedicated file
- ✅ Centralized MQTT communication system
- ✅ Dynamic Rule Engine that responds to sensor data
- ✅ Seasonal daily routines (loaded from Excel files)
- ✅ Automatic technical event logging (one per season)
- ✅ Clear system documentation & visualizations

---

## 🔄 General System Flow

```text
1. Time & Environment Update (via Environment Manager)
2. Sensors Read Data (Temperature, Motion, Light, etc.)
3. Sensors Publish Data via MQTT
4. MQTT Client Receives Data
5. Sensor Manager Updates Sensor Values
6. Rule Engine Evaluates Rules (If temperature > 26, turn on AC)
7. Matching Rules Trigger Device Commands
8. Devices Receive Commands via MQTT
9. Device Manager Updates Device States
10. Devices Perform Actions (Turn on, Adjust, etc.)
11. Each Action Logged to Technical Event Log
12. Dashboard (Optional) Displays Current Status
```

---

## 📡 Expanded MQTT Section

### 📑 Recommended MQTT Topic Structure

```text
apartment/<room>/<device_type>/<device_id>
```
Example:
```
apartment/living_room/lights/LIGHT_LIVINGROOM_01
apartment/kitchen/temperature_sensor/TEMP_KITCHEN_01
```

### 📤 Example Sensor Data Message (Published by Sensors)

```json
{
    "sensor_id": "TEMP_LIVINGROOM_01",
    "room": "Living Room",
    "type": "Temperature Sensor",
    "value": 23.5,
    "timestamp": "2025-03-06T12:00:00"
}
```

### 📥 Example Command Message (Published to Devices)

```json
{
    "device_id": "AC_LIVINGROOM_01",
    "room": "Living Room",
    "command": "turn_on",
    "parameters": {
        "temperature": 22
    },
    "timestamp": "2025-03-06T12:00:01"
}
```

### 📥 Example MQTT Message Handler (Python Code Block)

```python
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload.decode('utf-8'))

    if "sensor" in topic:
        sensor_manager.update_sensor(payload)
        rule_engine.evaluate_rules(payload)
    elif "device" in topic:
        device_manager.handle_device_command(payload)
```

### 📤 Example Publishing Sensor Data

```python
import json
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("mqtt_broker_address")

sensor_data = {
    "sensor_id": "MOTION_KITCHEN_01",
    "room": "Kitchen",
    "type": "Motion Sensor",
    "value": "detected",
    "timestamp": "2025-03-06T12:00:00"
}

client.publish("apartment/kitchen/motion_sensor/MOTION_KITCHEN_01", json.dumps(sensor_data))
```

### 📥 Example Receiving Device Command

```python
def handle_device_command(command_data):
    device_id = command_data['device_id']
    command = command_data['command']
    parameters = command_data.get('parameters', {})

    device = device_manager.get_device_by_id(device_id)
    if device:
        device.receive_command(command, parameters)
```

---

## ✅ Final System Highlights

| Feature | Status |
|---|---|
| Modular Sensors & Devices | ✅ |
| Central MQTT Bus | ✅ |
| Dynamic Rules (Configurable per Season) | ✅ |
| Seasonal Routine Files | ✅ |
| Technical Event Logs | ✅ |
| Dashboard (Optional) | ✅ |
| Full Documentation | ✅ |

---

## 📥 Want More?

Let me know if you want this **as a Markdown file** for easy sharing or inclusion in your project documentation.
