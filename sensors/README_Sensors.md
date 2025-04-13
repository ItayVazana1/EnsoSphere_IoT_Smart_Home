# 🧠 EnsoSphere – Sensors Module

## 📦 Purpose
The `sensors/` module contains all sensor classes used by the simulator to evaluate environmental and logical conditions per tick. Each sensor reads from the generated `state_json` and contributes key-value pairs to the DB and MQTT layer.

---

## 🧭 Integration Context
- Sensors are evaluated during each tick by the simulator.
- Each sensor implements a unified `evaluate(state_json, room_engine)` method.
- Outputs are collected and published via MQTT and inserted into the `sensor_outputs` table in MySQL.

---

## 🗺️ Room Mapping Configuration
- The sensor-to-room association is defined in `config/sensor_room_map.json`.
- Each sensor is mapped to a specific room (e.g., `LivingRoom`, `Bathroom1`, etc.).
- The simulator loads this map to instantiate room-based sensors accordingly.
- Special sensors like `no_motion_all_rooms` are marked as `"room": "Global"`.

Example entry:
```json
{
  "LivingRoom": [
    {"id": "motion_livingroom", "type": "motion"},
    {"id": "temperature_livingroom", "type": "temperature"},
    {"id": "noise_livingroom", "type": "noise"}
  ],
  "Global": [
    {"id": "no_motion_all_rooms", "type": "logical"}
  ]
}
```

### 📌 Sensor Distribution by Room

#### `LivingRoom`
- `motion_livingroom` → Detects presence (affects lights, TV, etc.)
- `temperature_livingroom` → Impacts heating/cooling decisions
- `noise_livingroom` → Used to determine room activity level

#### `Kitchen`
- `motion_kitchen` → Triggers lights, cooking routines
- `temperature_kitchen` → Environmental data for appliances
- `humidity_kitchen` → Ventilation or cooking moisture tracking
- `gas_kitchen` → Detects dangerous gas levels

#### `Balcony`
- `motion_balcony` → Outdoor activity detection
- `temperature_balcony` → Weather impact monitoring
- `noise_balcony` → Environmental or social activity

#### `ParentsRoom`
- `motion_parentsroom`
- `temperature_parentsroom`
- `noise_parentsroom`

#### `KobeRoom`
- `motion_koberoom`
- `temperature_koberoom`
- `noise_koberoom`

#### `GavriellaRoom`
- `motion_gavriellaroom`
- `temperature_gavriellaroom`
- `noise_gavriellaroom`

#### `Bathroom1`
- `motion_bathroom1`
- `temperature_bathroom1`
- `humidity_bathroom1`

#### `Bathroom2`
- `motion_bathroom2`
- `temperature_bathroom2`
- `humidity_bathroom2`

#### `Global`
- `no_motion_all_rooms` → Aggregated sensor used for global inactivity checks (e.g., activating security mode)

---

## 🧱 Sensors Overview

### 🧩 `sensor.py`
**Base Sensor Class**
- Defines the standard `evaluate()` interface.
- Handles room/global flags.

### 🔊 `noise_sensor.py`
**Room-based noise measurement.**
- Output: `noise_<room>` → decibel level (float)
- Depends on `room_engine` logic for noise sources.

### 🌡️ `temperature_sensor.py`
**Room-based temperature measurement.**
- Output: `temperature_<room>` → °C (float)
- Reflects weather, HVAC, and room insulation.

### 💨 `humidity_sensor.py`
**Room-based humidity measurement.**
- Output: `humidity_<room>` → % humidity (float)
- Affected by environment and device activity (e.g., fans).

### 🛑 `gas_sensor.py`
**Room-based gas level detector.**
- Output: `gas_<room>` → gas concentration (float)
- Simulates air quality and gas presence.

### 🕺 `motion_sensor.py`
**Motion detection per room.**
- Output: `motion_<room>` → `True` or `False`
- Based on occupant presence via `room_engine`.

### 🧠 `logical_sensor.py`
**Logical condition evaluation.**
- Currently supports: `no_motion_all_rooms`
- Aggregates multiple motion sensors to detect apartment-wide inactivity.

### 🧮 `sensors_registry.py`
**Sensor Loader and Registry.**
- Central function: `get_all_sensors()`
- Returns a list of sensor instances.
- Used by the simulator to evaluate all sensors generically.

---

## 📤 Output Format
Each sensor returns a dictionary:
```python
{
    "sensor_name": sensor_value
}
```

These are combined into a single `sensor_outputs` dict that becomes part of the `state_json` per tick.

---

## ✅ Status
✅ All sensor classes implemented and integrated.  
✅ Full support for MQTT publishing and DB insertion.  
✅ Unified evaluation flow via registry.  
✅ Room map config successfully links all sensors to real rooms.  
✅ Coverage confirmed across all rooms in the smart apartment.

Ready for use in simulation and rule-based automation.

---

_Updated: April 13, 2025_
