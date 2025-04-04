
# 📐 EnsoSphere – Data & Message Formatting Guide

> This document defines the **standardized formats** used throughout the EnsoSphere Smart Apartment Simulation System.
It includes schemas for rules, MQTT messaging, simulation states, character routines, and database structures.

---

## 🧠 Rule Format (rules.json)

Each rule is a JSON object specifying its ID, description, trigger conditions, and resulting actions.

```json
{
  "rule_id": "lights_auto_night_kitchen",
  "description": "Turn on kitchen light at night if motion detected",
  "trigger": {
    "all": [
      {"sensor": "motion_kitchen", "equals": true},
      {"env": "is_daytime", "equals": false}
    ]
  },
  "actions": [
    {"device": "lights_kitchen", "command": {"status": "on"}}
  ]
}
```

### 🔹 Trigger Options:
- `sensor`: matches value from `sensor_outputs`
- `env`: matches a key directly from `state_json` (e.g., `is_daytime`)
- Logical operators: `all`, `any`, `not`
- Future: `room_occupied("Living Room")`

### 🔸 Action Format:
```json
{"device": "<device_id>", "command": { "status": "on" }}
```

---

## 📡 MQTT Messaging Format

### 🔹 Publish Request (CoreLogic → Device):
```json
{
  "device_id": "tv_living_room",
  "command": {
    "status": "on",
    "volume": 30
  },
  "state_id": 145
}
```

### 🔸 Optional Device Acknowledgment (Device → CoreLogic):
```json
{
  "device_id": "tv_living_room",
  "ack": true,
  "executed_command": {
    "status": "on",
    "volume": 30
  },
  "state_id": 145,
  "timestamp": "2025-04-01T13:42:00"
}
```

---

## 📅 Routine File Format (Excel, per character × season)

Each routine file contains the full 24-hour behavior of a character in **30-minute intervals**.

### 🔹 Columns:

| Column        | Description                        |
|---------------|------------------------------------|
| `Time`        | 24-hour clock in HH:MM format       |
| `Room`        | Room name or context (`Bathroom`)   |
| `Activity`    | Optional: text describing the task  |
| `Triggers`    | Optional: linked sensor behavior    |
| `Notes`       | Optional: logic hints or overrides  |

> Each routine file should have **48 rows** (30 min x 24 hours)

---

## 🧾 state_json Format (Simulation Output)

```json
{
  "timestamp": "2025-08-01T07:30:00",
  "season": "Summer",
  "is_daytime": true,
  "temperature": 31.5,
  "weather": "Sunny",
  "occupants": [
    { "name": "David", "location": "Living Room" }
  ],
  "rooms": [
    { "name": "Living Room", "occupants": ["David"] }
  ],
  "house_status": {
    "is_empty": false,
    "active_rooms": ["Living Room"]
  }
}
```

> Used internally and stored in the `state_raw` DB table per tick.

---

## 🧱 SQLite Table Schemas (Key Fields)

### 🔹 `state_raw`
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
timestamp TEXT
simulation_time TEXT
state_json TEXT
processed_by_core INTEGER DEFAULT 0
```

### 🔹 `sensor_outputs`
```sql
state_id INTEGER
sensor_id TEXT
value TEXT
```

### 🔹 `rule_triggers`
```sql
state_id INTEGER
rule_id TEXT
triggered INTEGER
conditions_json TEXT
actions_json TEXT
```

### 🔹 `device_states`
```sql
device_id TEXT PRIMARY KEY
state_json TEXT
last_updated TEXT
```

---

## 🧩 Data Flow Summary

| Component    | Input                        | Output                         |
|--------------|------------------------------|--------------------------------|
| Simulator    | Time, weather, routines      | `state_json` → `state_raw`     |
| CoreLogic    | `state_json`, sensors, rules | `rule_triggers`, MQTT, devices |
| WebUI        | `state_id`                   | Unified snapshot               |

---

## ✅ Best Practices

- Use `state_id` as the atomic unit for all tick operations
- Store full JSONs as `TEXT` fields (stringified)
- Maintain naming conventions for sensors/devices (e.g. `motion_kitchen`, `lights_livingroom`)
- All MQTT messages should include `state_id` for traceability

---

This formatting guide ensures consistent development, validation, and interop across the entire EnsoSphere system.
