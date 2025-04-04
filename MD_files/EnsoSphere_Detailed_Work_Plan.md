
# 📅 EnsoSphere – Full Project Work Plan

> **Target Completion Date:** Early May (before May 1st)  
> **Start Date:** April 1st

This work plan outlines each development phase for the EnsoSphere Smart Apartment Simulation system. Tasks are grouped by phase and ordered chronologically. Each section includes the goal, key files, test strategy, and estimated duration.

---

## 🔵 Phase 1: Bootstrap Setup
**🎯 Goal:** Establish the project structure and Docker environment for all containers.

- Create the full folder structure (`simulator/`, `corelogic/`, `webui/`, etc.)
- Write `.env` with tick interval and paths.
- Validate `Dockerfile.simulator`, `Dockerfile.corelogic`, `Dockerfile.webui`
- Compose and run system with `docker-compose up`
- Ensure Mosquitto broker and SQLite container are live

**📄 Key Files:**  
`.env`, `docker-compose.yml`, `Dockerfile.*`

**🧪 Unified Test File:**  
`test_bootstrap.py`

**⏱ Estimated Time:** 2 days

---

## 🟠 Phase 2: Simulator Engine
**🎯 Goal:** Generate `state_json` every tick and insert it into the `state_raw` DB table.

- Simulate accelerated time
- Compute season, weather, is_daytime
- Track occupant locations via seasonal routine files
- Generate complete `state_json` with rooms, occupants, house status
- Write to SQLite

**📁 Expected Files:**  
- `simulator/time_manager.py`  
- `simulator/weather_engine.py`  
- `simulator/occupant_engine.py`  
- `simulator/state_builder.py`  
- `simulator/simulator_main.py`

**📌 Routines Format:**  
Planned structure: **4 files per character (1 per season)** = 5 characters × 4 = **20 routine files**. Final format to be determined.

**🧪 Unified Test File:**  
`test_simulator_tick.py`

**⏱ Estimated Time:** 5 days

---

## 🟡 Phase 3: CoreLogic Engine
**🎯 Goal:** Process ticks: interpret sensors, evaluate rules, control devices via MQTT.

- Load unprocessed `state_raw`
- Compute `sensor_outputs`
- Match rules from unified `rules_master.json`
- Send MQTT device commands
- Update `device_states` and `rule_triggers`
- Mark tick as `processed_by_core = 1`

**📁 Expected Files:**  
- `corelogic/db_connector.py`  
- `corelogic/sensor_manager.py`  
- `corelogic/rule_engine.py`  
- `corelogic/device_manager.py`  
- `corelogic/mqtt_publisher.py`  
- `corelogic/corelogic_main.py`

**📌 Rule Design Strategy:**  
Use a **unified rule set** per device based on **functionality and thresholds**. No separate rules per season.

**🧪 Unified Test File:**  
`test_corelogic_tick.py`

**⏱ Estimated Time:** 6 days

---

## 🟢 Phase 4: Sensor Modules
**🎯 Goal:** Implement all sensor classes with proper MQTT integration and test hooks.

**📁 Sensor Files:**  
- `motion_sensor.py`, `temperature_sensor.py`, `humidity_sensor.py`  
- `gas_sensor.py`, `noise_sensor.py`, `door_main.py`  
- `pet_near_door.py`, `no_motion_all_rooms.py`

**🧪 Unified Test File:**  
`test_all_sensors.py`

**⏱ Estimated Time:** 4 days

---

## 🟣 Phase 5: Device Modules
**🎯 Goal:** Implement all actuator classes and ensure they support MQTT and logging.

**📁 Device Files:**  
- `lights.py`, `air_conditioner.py`, `tv_living_room.py`  
- `audio_system.py`, `door_pet.py`, `pet_feeder.py`  
- `robot_vacuum.py`, `door_lock.py`, `security_system.py`  
- `window.py`, `ventilation_fan.py`, `blinds.py`

**🧪 Unified Test File:**  
`test_all_devices.py`

**⏱ Estimated Time:** 4 days

---

## 🔴 Phase 6: WebUI Development
**🎯 Goal:** Visual dashboard that shows current tick status, devices, and rule activity.

- Build layout using React + Tailwind/Bootstrap
- Poll DB for latest `processed_by_core = 1` tick
- Render: occupants, environment, devices, rules

**📁 UI Components:**  
- `App.jsx`, `DashboardClient.js`  
- `RoomMap.jsx`, `DeviceCards.jsx`, `EnvironmentBar.jsx`, `RuleFeed.jsx`

**🧪 Unified Test File:**  
`test_webui_render.py`

**⏱ Estimated Time:** 5 days

---

## ⚫ Phase 7: Full Integration & Synchronization
**🎯 Goal:** Test complete tick flow across all components from simulator to WebUI.

- Run full tick loop
- Verify DB consistency via `state_id`
- Ensure WebUI displays expected snapshot

**🧪 Unified Test File:**  
`test_full_integration.py`

**⏱ Estimated Time:** 3 days

---

## ✳️ Phase 8: Optional Features & Enhancements
**🎯 Goal:** Add advanced features after system stability

- Tick replay via `state_id`
- WebUI timeline scrubber
- REST API or WebSocket push to UI
- Animations or MQTT visualizer

**🧪 Test File:** TBD

**⏱ Estimated Time:** 5 days

---

## ✅ Final Notes
- After each **major phase**, write a **single test file** that validates all logic in that folder.
- Rules will remain **device-based**, **season-independent**.
- Routine files will be organized by **character and season**.

