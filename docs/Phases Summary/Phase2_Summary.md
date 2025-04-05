# ✅ Phase 2 – Simulator Engine Core (State Generator)

## 🧠 Purpose
This phase focused on implementing the **core simulation engine** that produces realistic, time-based `state_json` snapshots of the smart apartment.  
The state reflects the occupants' behavior, room activity, weather, and environmental conditions, and is stored in the database at each tick.

---

## 🧱 Components Developed

### 1. `simulator_main.py`
- Main loop runner for the simulation ticks.
- Handles database connection, tick batching, printing state info, and storing in MySQL.
- Supports random date generation unless overridden in `.env`.
- Dynamically derives the season from the simulation date.
- Uses the `StateBuilder` class to construct the full `state_json`.

### 2. `time_manager.py`
- Manages simulated time progression by 30-minute intervals (configurable).
- Tracks current simulated datetime.
- Computes:
  - `season` (Winter/Spring/Summer/Autumn)
  - `is_daytime` (07:00–20:00 considered day)

### 3. `occupant_engine.py`
- Loads Excel routines for each character from `routines/`.
- Returns each character’s location based on time and season.
- Outputs:
  - `occupants` (with name + location)
  - `rooms` (grouped view by room → occupants)

### 4. `weather_engine.py`
- Provides current `weather` (e.g., sunny, rainy, cloudy) and `temperature` based on:
  - Season
  - Day vs night
- Supports randomization within seasonal ranges.

### 5. `house_engine.py`
- Tracks per-room activity.
- Determines:
  - `active_rooms` (rooms where at least one person is present)
  - `room_state` (each room marked active/inactive)
  - `is_empty` (true if apartment has no occupants)

### 6. `state_builder.py`
- Combines all above engines to generate a full, valid `state_json`.
- Includes:
  - Timestamps, simulation time
  - Weather, temperature
  - Occupants, rooms
  - House status block
  - `notes` metadata

### 7. `state_schema.py`
- Defines the official schema for `state_json`, for clarity and validation.

---

## 🧪 Testing & Validation
- Full integration tests using:
  - Live MySQL connection
  - Real routine files for all 5 characters (Excel)
- Simulated multiple tick cycles using batch size = 1 and tick delay = 5 seconds.
- Output verified visually and in database via Adminer.

---

## 🗃️ DB Table Updated

### `state_raw`
| Column           | Type         | Description                            |
|------------------|--------------|----------------------------------------|
| timestamp        | DATETIME     | Simulation tick datetime               |
| simulation_time  | VARCHAR      | Human-readable format (YYYY-MM-DD HH:MM) |
| season           | VARCHAR      | Season name                            |
| is_daytime       | BOOLEAN      | True if between 07:00 and 20:00        |
| temperature      | FLOAT        | Current temperature in Celsius         |
| weather          | VARCHAR      | Weather condition (e.g., Sunny)        |
| state_json       | LONGTEXT     | Full JSON dump of the state            |

---

## 📁 Related Files

| File | Purpose |
|------|---------|
| `simulator/simulator_main.py` | Main runner – orchestrates simulation |
| `simulator/time_manager.py` | Advances and interprets simulation time |
| `simulator/occupant_engine.py` | Loads character routines, outputs locations |
| `simulator/weather_engine.py` | Generates weather & temperature |
| `simulator/house_engine.py` | Tracks room activity status |
| `simulator/state_builder.py` | Builds full `state_json` using all engines |
| `simulator/state_schema.py` | Schema definition for `state_json` |
| `routines/*.xlsx` | Routines for David, Mishel, Gavriella, Kobe, Luna |

---

## ✅ Status
**Phase 2 Complete.**
Simulation engine is now producing structured, real-time state snapshots in sync with system time logic, and storing them to the database.

Ready to begin Phase 3 (Rule Engine & CoreLogic)!