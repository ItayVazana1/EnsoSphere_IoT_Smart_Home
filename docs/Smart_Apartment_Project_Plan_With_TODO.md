
# 🏡 Smart Apartment IoT Simulation - Comprehensive Project Plan & To-Do List

This document outlines a **detailed work plan** for the Smart Apartment IoT project, including:
- Step-by-step breakdown
- Estimated time for each step
- Key tips for success
- Specific To-Do lists for every phase

---

## 📅 Project Timeline - Estimated: 12-14 Weeks

| Phase | Description | Estimated Time |
|---|---|---|
| 1 | Initial Planning & System Design | 1-1.5 Weeks |
| 2 | Environment Manager & Simulation | 1-1.5 Weeks |
| 3 | Core Device & Sensor Classes | 2 Weeks |
| 4 | MQTT Communication & Message Flow | 1-1.5 Weeks |
| 5 | Rule Engine & Logic Processing | 1.5-2 Weeks |
| 6 | Seasonal Daily Routine Simulation | 1-1.5 Weeks |
| 7 | Integration Testing | 1-1.5 Weeks |
| 8 | Technical Event Log Generation | 1 Week |
| 9 | Documentation & Final Packaging | 0.5-1 Week |

---

## 📝 Phase 1 - Initial Planning & System Design

### Goal
- Define rooms, devices, sensors, and key interactions.
- Finalize project folder structure.
- Create base configuration files.

### Key Deliverables
- `config.yaml` with room and device/sensor definitions.
- Final folder & file structure.
- Device & sensor type lists.

### Key Tips
- Focus on modularity – each device/sensor stands alone.
- Think about how seasonal changes will affect automation.
- Lock in your MQTT topic structure early.

### ✅ To-Do List
- [ ] Finalize room list
- [ ] Finalize device types and sensor types
- [ ] Draft `config.yaml`
- [ ] Create folder & file structure
- [ ] Document MQTT topic naming convention

---

## 📝 Phase 2 - Environment Manager & Simulation

### Goal
- Create a module to simulate time, day/night cycle, and seasonal weather.

### Key Deliverables
- `environment_manager.py` (time/weather simulator).

### Key Tips
- Time should be accelerated (1 minute = X seconds).
- Weather should influence window, blinds, and HVAC logic.
- Allow querying current light levels and temperature.

### ✅ To-Do List
- [ ] Implement accelerated time simulation
- [ ] Add seasonal temperature & weather generation
- [ ] Add daylight cycle logic (sunrise/sunset)
- [ ] Expose environment data to devices/sensors

---

## 📝 Phase 3 - Core Device & Sensor Classes

### Goal
- Create flexible base classes for all devices and sensors.

### Key Deliverables
- `base_device.py` and `base_sensor.py`
- Device classes for: AC, Blinds, Lights, Robot Vacuum, Pet Feeder
- Sensor classes for: Motion, Temperature, Light, Humidity, Noise, Door

### Key Tips
- Each device should support "receive_command".
- Each sensor should support "read_value".
- Base classes should handle room, id, and type.

### ✅ To-Do List
- [ ] Create `base_device.py` and `base_sensor.py`
- [ ] Implement at least 5 devices
- [ ] Implement at least 5 sensors
- [ ] Ensure every class logs actions for debugging

---

## 📝 Phase 4 - MQTT Communication & Message Flow

### Goal
- Build central MQTT client to handle publishing and subscribing.

### Key Deliverables
- `mqtt_client.py`

### Key Tips
- Use consistent topic format (e.g., `apartment/living_room/light`).
- Log every received/sent message.
- Support both sensor data and device commands.

### ✅ To-Do List
- [ ] Implement MQTT client
- [ ] Define topic schema
- [ ] Connect sensor reads to MQTT publishes
- [ ] Connect device commands to MQTT messages

---

## 📝 Phase 5 - Rule Engine & Logic Processing

### Goal
- Implement the central rule engine to link sensor data to device actions.

### Key Deliverables
- `rule_engine.py`
- Example rules in `default_rules.json`

### Key Tips
- Rules should be data-driven (no hardcoded logic).
- Support flexible conditions (`greater_than`, `less_than`, etc.).
- Rules should trigger device actions via DeviceManager.

### ✅ To-Do List
- [ ] Define rule schema
- [ ] Implement rule evaluation engine
- [ ] Implement connection to SensorManager
- [ ] Implement connection to DeviceManager
- [ ] Load rules from file

---

## 📝 Phase 6 - Seasonal Daily Routine Simulation

### Goal
- Create system that reads daily routine files and triggers matching sensor events.

### Key Deliverables
- Daily routine processors for all 4 seasons

### Key Tips
- Each row in the Excel should trigger a sensor reading or a device command.
- Time-of-day handling should align with environment manager.

### ✅ To-Do List
- [ ] Load daily routines from Excel
- [ ] Simulate time-based sensor triggers
- [ ] Trigger rules based on simulated events
- [ ] Handle seasonal differences (heating vs cooling)

---

## 📝 Phase 7 - Integration Testing

### Goal
- Ensure devices, sensors, rules, and environment interact correctly.

### Key Deliverables
- Full system simulation log for at least 1 day per season.

### Key Tips
- Use clear logging for every action (sensor read, rule evaluation, device command).
- Test each room separately before full integration.

### ✅ To-Do List
- [ ] Test each room independently
- [ ] Test each rule
- [ ] Test day/night transitions
- [ ] Test weather-driven events
- [ ] Run full 24-hour simulation

---

## 📝 Phase 8 - Technical Event Log Generation

### Goal
- Automatically generate detailed event logs for each simulation run.

### Key Deliverables
- Seasonal `event_log_<season>.csv` files.

### Key Tips
- Every log entry should include timestamp, room, device, action, and trigger.
- Align format with the event tables you provided.

### ✅ To-Do List
- [ ] Implement central logger for events
- [ ] Standardize log format
- [ ] Automatically save logs per season
- [ ] Review logs for completeness

---

## 📝 Phase 9 - Documentation & Final Packaging

### Goal
- Create comprehensive documentation and archive all deliverables.

### Key Deliverables
- README.md
- Final ZIP including all code, logs, and documentation

### Key Tips
- Document every folder, file, and class.
- Include system overview diagram.
- Provide sample output logs for each season.

### ✅ To-Do List
- [ ] Write README.md
- [ ] Document all major files & classes
- [ ] Create system flow diagram
- [ ] Package all files into final ZIP

---

## 🔥 Final Tip
Stay modular and focus on **one room and one rule at a time** in early stages. Once the system works for a simple case (e.g., Living Room lights on motion), scaling to other rooms and rules will be fast.

---
