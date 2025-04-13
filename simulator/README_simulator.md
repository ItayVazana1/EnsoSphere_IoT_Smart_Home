
# 🧠 EnsoSphere – Simulator Module

## 📦 Purpose
The `simulator/` module is responsible for generating the simulation ticks that drive the entire smart apartment system. It simulates environment conditions, occupant behavior, sensor readings, and produces the main `state_json` structure that is used by the CoreLogic engine to evaluate rules and control devices.

---

## 🧭 System Flow Overview

1. **Startup Phase**:
   - Connects to MySQL and MQTT.
   - Selects a random date and determines the current season.
   - Loads routines, sensors, devices, and environment configuration.

2. **Tick Loop Execution**:
   - At each tick (one every X seconds), the simulator builds a new system state using several internal engines:
     - `TimeManager` → Calculates current tick time, day, slot.
     - `WeatherEngine` → Generates weather and temperature for the day.
     - `OccupantEngine` → Determines character location and movement.
     - `RoomEngine` → Holds per-room logic and state.
     - `HouseEngine` → Handles room definitions, features.
     - `SensorPublisher` → Evaluates all sensors and produces output.
     - `DeviceStateFetcher` → Pulls previous device states from DB.
     - `StateBuilder` → Combines everything into one `state_json` dict.

3. **Data Output**:
   - Publishes sensor values to MQTT broker.
   - Inserts the full tick (`state_json`) into the `state_raw` table in MySQL.

---

## 📁 File Overview

### 🧩 `simulator_main.py`
Main entry point of the simulation engine.
- Handles the full execution loop per tick.
- Publishes sensor data and stores tick in DB.

### ⏰ `time_manager.py`
- Computes the current simulation time.
- Converts ticks to hour and day blocks.

### 🌦️ `weather_engine.py`
- Randomized generator for weather per day.
- Affects external temperature and environmental conditions.

### 👥 `occupant_engine.py`
- Loads seasonal routines from Excel.
- Determines character location based on time and date.

### 🏠 `house_engine.py`
- Defines all rooms in the apartment.
- Returns valid room list and room-related metadata.

### 🧩 `room_engine.py`
- Combines occupant, environment, and device info per room.
- Supports sensor evaluations based on full context.

### 🌡️ `sensor_publisher.py`
- Loads and evaluates all registered sensors.
- Publishes results to MQTT and returns `sensor_outputs`.

### 📥 `device_state_fetcher.py`
- Pulls latest device state from DB to feed into simulation.
- Ensures state_json has accurate `device_states` block.

### 🏗️ `state_builder.py`
- Creates the final unified `state_json` structure.
- Merges sensor, occupant, environment, and device data.

### 📐 `state_schema.py`
- Provides validation and formatting helpers for the state JSON.

### 📡 `mqtt_client.py`
- Lightweight MQTT client for simulator use.
- Publishes to the `sensor/<sensor_id>` topic.

---

## 📦 `state_json` Structure
The simulator produces a `state_json` object every tick, structured like so:

```json
{
  "timestamp": "2025-03-09 06:30:00",
  "season": "Winter",
  "weather": "Rainy",
  "outside_temperature": 6.5,
  "occupants": { "David": "Kitchen", ... },
  "sensor_outputs": { "motion_kitchen": true, ... },
  "device_states": { "lights_kitchen": {"status": "on"}, ... }
}
```

This object is inserted into `state_raw` and used by CoreLogic to evaluate rules.

---

## 🧠 Integration Points

### 🐬 MySQL
- All simulator-generated states are written to `state_raw`.
- Table: `state_raw(id, state_json, processed_by_core, processed_at)`

### 📡 MQTT
- Each sensor publishes to a unique topic like `sensor/motion_kitchen`.
- Only raw sensor values are published (not full state).

---

## ✅ Module Status
✅ Fully integrated with MySQL + MQTT.  
✅ Tick loop functional and stable.  
✅ Seasonal logic working with full Excel-based occupant routines.  
✅ Weather, time, and house engines operational.  
✅ All sensors and devices initialized correctly.  
✅ `state_json` validated and compatible with CoreLogic expectations.

The simulator is ready for production-like testing with the CoreLogic engine.

---

_Updated: April 13, 2025_
