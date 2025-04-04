# 📂 EnsoSphere – Code File Inventory (Extended)

> This document describes the purpose and status of each source file in the Smart Apartment IoT Simulation system.  
It serves as a living map of the codebase to assist with navigation, onboarding, and maintenance.

---

## 🧱 Project Structure Overview

```
EnsoSphere/
├── simulator/            # Simulated environment and time
├── corelogic/            # Rule engine, sensors, devices, MQTT
├── sensors/              # All sensor classes
├── devices/              # All actuator classes
├── occupants/            # Character models and behavior
├── rooms/                # Room logic and mapping
├── tests/                # Unit and integration tests
├── webui/                # React dashboard interface
├── mqtt/                 # Mosquitto config
├── data/                 # SQLite DB and logs
├── rules/                # Automation rules in JSON
├── routines/             # Seasonal character schedules
├── assets/               # Visual assets (e.g., WebUI cover image)
├── docs/                 # Technical documentation and design specs
├── docker/               # Optional Dockerfiles per container
└── docker-compose.yml    # Multi-container system setup
```

---

## 📁 simulator/

| File | Purpose | Status |
|------|---------|--------|
| `time_manager.py` | Manages accelerated simulation time and current datetime | ⏳ Planned |
| `weather_engine.py` | Generates weather, temperature, and day/night flag | ⏳ Planned |
| `occupant_engine.py` | Determines occupant locations based on routines | ⏳ Planned |
| `state_builder.py` | Builds `state_json` with room mappings and status | ⏳ Planned |
| `simulator_main.py` | Main tick loop – creates and writes full simulation state | ⏳ Planned |

---

## 📁 corelogic/

| File | Purpose | Status |
|------|---------|--------|
| `db_connector.py` | Handles DB access and queries | ⏳ Planned |
| `sensor_manager.py` | Evaluates sensor outputs from state | ⏳ Planned |
| `rule_engine.py` | Applies automation rules and matches triggers | ⏳ Planned |
| `device_manager.py` | Simulates devices, updates their states | ⏳ Planned |
| `mqtt_publisher.py` | Publishes MQTT commands to broker | ⏳ Planned |
| `corelogic_main.py` | Main CoreLogic loop per tick | ⏳ Planned |

---

## 📁 sensors/

| File | Purpose |
|------|---------|
| `base_sensor.py` | Abstract base class for all sensors |
| `motion_sensor.py` | Detects motion in rooms |
| `temperature_sensor.py` | Reads room temperature |
| `humidity_sensor.py` | Detects humidity levels |
| `gas_sensor.py` | Detects gas presence |
| `noise_sensor.py` | Monitors sound levels |
| `weather_sensor.py` | Reports environmental weather |
| `pet_near_door.py` | Detects pet proximity near entrance |
| `door_main.py` | Detects open/close status of main door |
| `no_motion_all_rooms.py` | Logical sensor – checks if all rooms are motionless |

---

## 📁 devices/

| File | Purpose |
|------|---------|
| `base_device.py` | Abstract base class for all actuators |
| `lights.py` | Controls light status in rooms |
| `air_conditioner.py` | Controls cooling system |
| `audio_system.py` | Controls audio playback |
| `blinds.py` | Opens or closes blinds |
| `tv_living_room.py` | Operates the living room TV |
| `door_pet.py` | Smart pet door for Luna |
| `pet_feeder.py` | Dispenses food for Luna |
| `robot_vacuum.py` | Activates cleaning sequence |
| `door_lock.py` | Locks/unlocks the main entrance |
| `security_system.py` | Controls alarm/security mode |
| `window.py` | Opens/closes smart windows |
| `ventilation_fan.py` | Adjusts air circulation |

---

## 📁 occupants/

| File | Purpose |
|------|---------|
| `base_occupant.py` | Base class for all characters (people, pets) |
| `occupant_factory.py` | Optional factory for building occupants from routine files |

---

## 📁 rooms/

| File | Purpose |
|------|---------|
| `base_room.py` | Optional base class for Room logic (metadata, sensors, devices) |

---

## 📁 tests/

| File | Purpose |
|------|---------|
| `test_motion_sensor.py` | Unit test for motion sensor logic |
| `test_temperature_sensor.py` | Unit test for temperature logic |
| `test_rule_engine.py` | Tests rule evaluation across ticks |
| `test_device_states.py` | Validates device actions and MQTT responses |
| `test_simulator_routine.py` | Validates seasonal routine parsing |
| `test_no_motion_logic.py` | Verifies logical sensors like `no_motion_all_rooms` |
| `test_full_tick_cycle.py` | End-to-end test for simulator + corelogic integration |

---

## 📁 webui/ (React)

| File | Purpose |
|------|---------|
| `DashboardClient.js` | Fetches and parses current tick data |
| `EnvironmentBar.jsx` | Renders weather, season, and clock |
| `RoomMap.jsx` | Displays layout of rooms and sensor activity |
| `DeviceCards.jsx` | Shows current state of all devices |
| `RuleFeed.jsx` | Displays recent rule triggers |
| `App.jsx` | Entry point and routing layout |

---

## 📁 assets/

- `Final_Cover.PNG` – Project cover image for README and UI
- (Future icons, room layouts, UI assets)

---

## 📁 docker/

| File | Purpose |
|------|---------|
| `Dockerfile.simulator` | Build instructions for the simulator container |
| `Dockerfile.corelogic` | Build instructions for core logic container |
| `Dockerfile.webui` | WebUI container (React + Nginx or Node) |
| (Others as needed)

---

## 📄 Root-Level Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Multi-container setup and network configuration |
| `.env` | Environment config for secrets, delays, MQTT, DB path |
| `README_EnsoSphere.md` | Project overview |
| `DEVELOPMENT_GUIDELINES.md` | Team coding and workflow standards |
| `CODE_FILE_INVENTORY_EXTENDED.md` | This file – full file documentation |

---

The file inventory is continuously evolving with development.  
Please update this document whenever new modules are added or responsibilities change.
