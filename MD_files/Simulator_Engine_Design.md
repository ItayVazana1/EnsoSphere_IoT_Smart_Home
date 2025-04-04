# Simulator Engine – Structure, Logic & Output Design

## 🧠 Purpose
The Simulator is responsible for **creating the virtual world** of the smart apartment: time, environment, occupants, and daily behavior patterns. It drives the simulation by emitting `state_json` at every tick.

---

## 📦 Responsibilities
- Manage accelerated simulation time (e.g., 1 tick = 30 simulated minutes)
- Compute season, daylight, and weather
- Simulate each occupant's movement based on daily routine
- Generate the complete `state_json` for each tick
- Insert the generated snapshot into the `state_raw` table

---

## 🔁 Execution Loop
1. Get current simulated time and date
2. Determine:
   - Season (by date or preset)
   - Weather (stochastic or predefined by season)
   - Is it day or night?
3. Move occupants according to their current routine
4. Build room occupancy map
5. Create `state_json`
6. Write to SQLite: `INSERT INTO state_raw`

---

## 🧱 State JSON Format (Output Example)
```json
{
  "timestamp": "2025-08-01T07:30:00",
  "season": "Summer",
  "is_daytime": true,
  "temperature": 31.5,
  "weather": "Sunny",
  "occupants": [
    { "name": "David", "location": "Living Room" },
    { "name": "Luna", "location": "Near Door" }
  ],
  "rooms": [
    { "name": "Living Room", "occupants": ["David"] },
    { "name": "Entrance", "occupants": ["Luna"] }
  ],
  "house_status": {
    "is_empty": false,
    "active_rooms": ["Living Room", "Entrance"]
  }
}
```

---

## 🔧 Core Components

### 1. Time Manager
- Simulated datetime engine (fast-forwarded clock)
- Supports days, months, seasons
- Tick interval = X real seconds = Y simulated minutes

### 2. Weather Engine
- Generates `weather`, `temperature`, `is_daytime`
- Season-based probabilities (sunny, cloudy, rainy)
- Optional: support static weather per day (scripted)

### 3. Occupant Engine
- Models each character with a routine per season
- Inputs: list of actions by time blocks (e.g., 07:00–07:30 = Bathroom)
- Outputs: current location of each occupant

### 4. Room Mapper
- Maps each room to its active occupants
- Used for logical sensors (room_occupied, noise_level, etc)

---

## 📋 Development Tasks

### Phase A: Time & Environment
- [ ] Implement time acceleration engine
- [ ] Build season and daylight calculation logic
- [ ] Create weather generator with seasonal bias

### Phase B: Routine Execution
- [ ] Define per-character routines (via JSON or CSV)
- [ ] Parse current time → determine each occupant's location
- [ ] Handle edge cases (asleep, transitions, pet behavior)

### Phase C: Output Builder
- [ ] Generate `state_json` with all fields
- [ ] Derive rooms and house status automatically
- [ ] Write to SQLite (`state_raw`)

### Phase D: Advanced Features
- [ ] Add optional mode for fixed scripted routines
- [ ] Allow fast-forward and replay
- [ ] Simulate external events (guest arrives, doorbell rings)

---

## 🧩 Output Integrity Notes
- `state_json` should always include all fields
- Occupants and rooms must stay in sync
- Maintain time accuracy across ticks
- Track unique `tick_id` for debugging

---

This document defines the engine behind the simulation logic of the smart apartment system. It feeds all other components with structured, consistent world state snapshots.
