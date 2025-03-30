
# 📦 Smart Apartment IoT – Component Inventory (Corrected)

## 🟦 Sensor Modules (Simulated Inputs)

| Sensor ID               | Type               | Description                                      | Status         |
|------------------------|--------------------|--------------------------------------------------|----------------|
| `motion_sensor`        | Motion             | Detects movement in rooms                        | ✅ Implemented |
| `gas_sensor`           | Gas                | Detects gas levels or leaks                      | ✅ Implemented |
| `humidity_sensor`      | Humidity           | Measures humidity level                          | ✅ Implemented |
| `temperature_sensor`   | Temperature        | Measures room temperature                        | ✅ Implemented |
| `noise_sensor`         | Noise              | Measures sound levels (e.g. barking)             | ✅ Implemented |
| `weather_sensor`       | Weather            | Provides current weather condition               | ✅ Implemented |
| `door_main_sensor`     | Door Contact       | Detects if main door is opened/closed            | 🆕 NEW          |
| `pet_near_door_sensor` | Pet Proximity      | Detects Luna near main door                      | 🆕 NEW          |
| `no_motion_all_rooms`  | Logical (Virtual)  | True if no motion detected anywhere              | 🆕 NEW          |

---

## 🟩 Actuator Modules (Devices)

| Device ID              | Type             | Description                                       | Status         |
|------------------------|------------------|---------------------------------------------------|----------------|
| `air_conditioner`      | Air Conditioner  | Controls cooling system                           | ✅ Implemented |
| `audio_system`         | Audio System     | Controls music/audio playback                     | 🆕 NEW          |
| `blinds`               | Blinds           | Opens/closes blinds in room                       | ✅ Implemented |
| `door_lock`            | Door Lock        | Controls locking/unlocking of main entrance       | ✅ Implemented |
| `door_pet`             | Pet Door         | Smart door for pet entry/exit                     | 🆕 NEW          |
| `lights`               | Lights           | Turns lights on/off per room                      | ✅ Implemented |
| `pet_feeder`           | Feeder           | Dispenses food for pet (Luna)                     | ✅ Implemented |
| `robot_vacuum`         | Robot Vacuum     | Cleans floor when house is empty                  | ✅ Implemented |
| `security_system`      | Security         | Controls alarm or security mode                   | ✅ Implemented |
| `tv_living_room`       | TV               | Controls living room television                   | 🆕 NEW          |
| `ventilation_fan`      | Ventilation Fan  | Adjusts airflow for air quality                   | ✅ Implemented |
| `window`               | Smart Window     | Opens/closes based on weather                     | ✅ Implemented |

---

## 🧠 Integration Summary

- All sensors publish to:
  ```
  MyHome/<room>/<sensor_type>/<sensor_id>
  ```

- All actuators subscribe to:
  ```
  MyHome/<room>/<device_type>/<device_id>
  ```

- Status updates from devices are published to:
  ```
  MyHome/<room>/<device_type>/<device_id>/status
  ```

- Fully integrated with MQTT communication, routine processing, and rule engine automation.

✅ **Inventory verified – system stable and consistent. Ready to finalize rules and seasonal scenarios.**
