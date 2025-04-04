# 🏡 Smart Apartment IoT Simulation

![Smart Apartment Cover](assets/Final_Cover.PNG)

Welcome to the **Smart Apartment IoT Simulation** project!  
This repository contains a fully modular and seasonal simulation of a smart home environment for a modern 5.5-room apartment near the sea 🌊, located on the 10th floor 🏢.

---

## 🎯 Project Goals

- Simulate **daily routines** across all four seasons (Winter, Spring, Summer, Autumn).
- Create a **virtual IoT ecosystem** with sensors, actuators, MQTT communication, and a centralized environment manager.
- Build a dynamic **rule engine** that reacts to sensor data and automates device behavior.
- Provide detailed **technical event logs** for each seasonal routine.
- Support real-time visualization via a **read-only dashboard** (optional).
- Ensure full **modularity**, scalability, and documentation.

---

## 🧠 Key Features

- 🌦️ Simulated time, daylight, seasons, and weather
- 🧩 Rule engine based on configurable JSON logic
- 🔧 Modular sensor and actuator simulation (motion, light, AC, etc.)
- 🔗 MQTT-based communication for full IoT simulation
- 📆 Seasonal Excel routines for human-like behavior
- 📊 CSV event logs for analysis and testing
- 📁 Full documentation and folder structure

---

## 🧰 Technologies Used

| Category | Tool/Library |
|----------|--------------|
| Language | Python 3.x |
| Messaging | MQTT (`paho-mqtt`) |
| Data Processing | `pandas`, `openpyxl`, `json` |
| Time & Environment | `datetime`, custom simulator |
| Logging | `logging`, custom logs |
| Visualization (optional) | `dashboard.py` |
| Documentation | Markdown (README, reports, summaries) |

---

## 📂 Project Structure

```bash
smart_apartment/
│
├── main.py
├── config.yaml
│
├── core/
│   ├── environment_manager.py
│   ├── mqtt_client.py
│   ├── rule_engine.py
│   └── scheduler.py
│
├── managers/
│   ├── device_manager.py
│   ├── sensor_manager.py
│   └── rule_manager.py
│
├── devices/
│   ├── base_device.py
│   ├── air_conditioner.py
│   ├── blinds.py
│   ├── lights.py
│   ├── robot_vacuum.py
│   └── pet_feeder.py
│
├── sensors/
│   ├── base_sensor.py
│   ├── motion_sensor.py
│   ├── temperature_sensor.py
│   ├── light_sensor.py
│   ├── humidity_sensor.py
│   └── noise_sensor.py
│
├── rules/
│   ├── rule_schema.json
│   └── default_rules.json
│
├── data/
│   ├── devices.json
│   ├── sensors.json
│
├── routines/
│   ├── Daily_routine_Winter_IoT.xlsx
│   ├── Daily_routine_Spring_IoT.xlsx
│   ├── Daily_routine_Summer_IoT.xlsx
│   └── Daily_routine_Autumn_IoT.xlsx
│
├── logs/
│   ├── system_log.txt
│   ├── errors_log.txt
│   ├── mqtt_log.txt
│   ├── Winter - Technical_Event_Table.csv
│   ├── Spring - Full Technical Event Table.xlsx
│   ├── Summer - Full Technical Event Table.xlsx
│   └── Autumn - Full Technical Event Table.xlsx
│
├── Archive/
│   ├── Smart_Apartment_Full_Report.md
│   ├── Smart_Apartment_Folder_Structure_and_Guide.md
│   ├── Smart_Apartment_Project_Plan_With_TODO.md
│   ├── Smart_Apartment_Full_Project_Summary.md
│   └── README_Smart_Apartment_Shopping_List.md
│
├── dashboard/
│   └── dashboard.py
│
├── utils/
│   ├── logger.py
│   ├── time_utils.py
│   └── mqtt_utils.py
│
├── assets/
│   └── Final_Cover.PNG
│
└── README.md
```

---

## 📅 Seasonal Simulation Overview

- **Winter** ❄️ – Early nightfall, heating needs, indoor lighting
- **Spring** 🌼 – Mild temperature, active routines, light usage
- **Summer** ☀️ – Heat management, ventilation, outdoor sensors
- **Autumn** 🍂 – Transition between summer & winter logic

---

## 🔁 System Flow Summary

```text
1. Environment Manager updates time & season
2. Sensors read data and publish via MQTT
3. MQTT Client receives data and forwards to SensorManager
4. SensorManager logs data and calls RuleEngine
5. RuleEngine checks for matching rules
6. If rule triggered, sends command to DeviceManager
7. Device receives command and acts (via MQTT)
8. Action is logged in seasonal event log
9. Dashboard reflects current state (optional)
```

---

## 📋 How to Use

1. Clone the repo and navigate to `smart_apartment/`
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the simulation:
    ```bash
    python main.py
    ```
4. Optional: Open the dashboard to monitor live status.

---

## 📘 Documentation

See the `docs/` folder for:
- 📖 Full device and room report
- 🧩 Rule engine structure and schema
- 📆 Project phases and timeline
- 🗂️ File structure and technical documentation

---

## 🚀 Credits & Contributors

Created as part of an **IoT Smart City Course** final project.  
Designed with clarity, modularity, and automation in mind 🧠💡

---

> For feedback, issues, or contributions – feel free to open a PR or contact the project author.