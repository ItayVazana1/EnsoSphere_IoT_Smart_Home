# 📐 EnsoSphere – `state_json` Schema Documentation

> This document describes the **official format** of the `state_json` object emitted by the Simulator at each tick.

---

## ✅ Required Fields

| Field             | Type   | Description |
|------------------|--------|-------------|
| `timestamp`       | string | UTC timestamp of the tick in ISO 8601 |
| `simulation_time` | string | Simulated time in readable format |
| `season`          | string | One of: `Winter`, `Spring`, `Summer`, `Autumn` |
| `is_daytime`      | bool   | True if daytime, False otherwise |
| `temperature`     | float  | Simulated temperature in °C |
| `weather`         | string | Weather type: `Sunny`, `Rainy`, etc. |
| `occupants`       | list   | Array of occupants with name + location |
| `rooms`           | list   | List of rooms with list of occupants |
| `house_status`    | dict   | Contains `is_empty` and `active_rooms` |
| `notes`           | dict   | Metadata (e.g. source = "simulator") |

---

## 🧍 Occupants Format

```json
{ "name": "David", "location": "Living Room" }
```

## 🏠 Rooms Format

```json
{ "name": "Living Room", "occupants": ["David"] }
```

## 🧠 House Status Format

```json
{
  "is_empty": false,
  "active_rooms": ["Living Room", "Kitchen"]
}
```

## 🗒️ Notes Format

```json
{
  "source": "simulator"
}
```

---

## 📌 Usage

- Written by: `simulator/simulator_main.py`
- Stored in: `state_raw.state_json` column (as stringified JSON)
- Read by: `CoreLogic`, `WebUI`, `Tests`

---

## ✅ Validation Tool

Implemented in: `simulator/state_schema.py`
Function: `validate_state_json(state_json: dict) -> bool`

---
