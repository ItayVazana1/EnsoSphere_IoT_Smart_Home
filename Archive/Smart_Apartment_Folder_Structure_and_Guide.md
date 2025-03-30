
# 📂 Smart Apartment - Full Directory Structure and File Guide

This document provides a comprehensive overview of the recommended directory structure and file roles for the Smart Apartment IoT Simulation System.

---

## 📁 Root Directory - `smart_apartment/`

### 📄 `main.py`
- 🚀 **Purpose:** Main entry point to the system. Initializes managers, loads configurations, connects to MQTT, and starts the main loop.
- 🔗 **Used by:** Everything.

### 📄 `config.yaml`
- ⚙️ **Purpose:** Defines core configurations such as rooms, initial devices/sensors, MQTT settings, and system parameters.
- 🔗 **Used by:** All managers and core components.

---

## 📁 core/

### 📄 `environment_manager.py`
- 🌤️ **Purpose:** Simulates time, seasons, daylight cycles, and weather conditions.
- 🔗 **Used by:** All devices, sensors, and the rule engine.

### 📄 `mqtt_client.py`
- 📡 **Purpose:** Manages MQTT connection, message publishing, and subscribing to relevant topics.
- 🔗 **Used by:** DeviceManager, SensorManager, RuleEngine.

### 📄 `rule_engine.py`
- 🧩 **Purpose:** Core logic processor - evaluates sensor data against rules to trigger device actions.
- 🔗 **Used by:** DeviceManager, SensorManager.

### 📄 `scheduler.py`
- ⏰ **Purpose:** Handles time-based routines and scheduled tasks (like morning routines per season).
- 🔗 **Used by:** DeviceManager.

---

## 📁 managers/

### 📄 `device_manager.py`
- 🛠️ **Purpose:** Maintains all devices, allows lookup by room or type, tracks device states, and updates devices via MQTT.
- 🔗 **Used by:** RuleEngine, Scheduler, Core.

### 📄 `sensor_manager.py`
- 🔎 **Purpose:** Maintains all sensors, reads data, stores last values, and forwards data to the rule engine.
- 🔗 **Used by:** RuleEngine, Core.

### 📄 `rule_manager.py`
- 📜 **Purpose:** Loads rules from JSON, validates them against schema, and supports dynamic rule updates.
- 🔗 **Used by:** RuleEngine.

---

## 📁 devices/

### 📄 `base_device.py`
- 🏗️ **Purpose:** Base class for all devices, defining common properties like ID, room, type, and state.
- 🔗 **Used by:** All specific device classes.

### 📄 Specific Devices (air_conditioner.py, blinds.py, etc.)
- 🔧 **Purpose:** Each file defines a specific type of device, inheriting from `base_device.py`, implementing its specific logic.
- 🔗 **Used by:** DeviceManager, RuleEngine.

---

## 📁 sensors/

### 📄 `base_sensor.py`
- 🏗️ **Purpose:** Base class for all sensors, defining common properties like ID, room, type, and last value.
- 🔗 **Used by:** All specific sensor classes.

### 📄 Specific Sensors (motion_sensor.py, temperature_sensor.py, etc.)
- 📡 **Purpose:** Each file defines a specific type of sensor, inheriting from `base_sensor.py`, implementing its own reading logic.
- 🔗 **Used by:** SensorManager, RuleEngine.

---

## 📁 rules/

### 📄 `rule_schema.json`
- 📏 **Purpose:** Defines the JSON schema to validate rules (sensor-to-device mappings and conditions).
- 🔗 **Used by:** RuleManager.

### 📄 `default_rules.json`
- 📜 **Purpose:** Contains the default set of rules (season-specific logic or general behavior rules).
- 🔗 **Used by:** RuleManager.

---

## 📁 data/

### 📄 `devices.json`
- 💾 **Purpose:** Persistent storage for all device configurations, states, and history.
- 🔗 **Used by:** DeviceManager.

### 📄 `sensors.json`
- 💾 **Purpose:** Persistent storage for all sensor configurations and historical readings.
- 🔗 **Used by:** SensorManager.

### 📄 Seasonal Event Logs (event_log_winter.csv, etc.)
- 📝 **Purpose:** CSV files documenting all technical events and system actions per season.
- 🔗 **Used by:** Whole system (for debugging and analysis).

---

## 📁 dashboard/

### 📄 `dashboard.py`
- 📊 **Purpose:** Optional read-only dashboard to visualize current device and sensor states across all rooms.
- 🔗 **Used by:** Optional - can run separately.

---

## 📁 utils/

### 📄 `logger.py`
- 🪵 **Purpose:** Central logging module for system logs, error logs, and MQTT logs.
- 🔗 **Used by:** Entire system.

### 📄 `time_utils.py`
- 🕒 **Purpose:** Helper functions for time manipulation, date formatting, and simulated clock handling.
- 🔗 **Used by:** Scheduler, EnvironmentManager.

### 📄 `mqtt_utils.py`
- 🧰 **Purpose:** Helper functions for parsing incoming MQTT messages and building outgoing MQTT payloads.
- 🔗 **Used by:** MQTT Client, DeviceManager, SensorManager.

---

## 📁 logs/

### 📄 `system_log.txt`
- 📄 **Purpose:** General system activity log (state changes, startup, shutdown, etc.).
- 🔗 **Used by:** Logger.

### 📄 `errors_log.txt`
- ❌ **Purpose:** Central error log capturing all exceptions and critical issues.
- 🔗 **Used by:** Logger.

### 📄 `mqtt_log.txt`
- 🛰️ **Purpose:** Logs all inbound and outbound MQTT traffic for debugging.
- 🔗 **Used by:** MQTT Client.

---

## Summary

This folder structure is designed for **scalability**, **maintainability**, and clear separation of concerns. Each file has a distinct responsibility, making it easy to update or replace individual components without affecting the whole system.

---
