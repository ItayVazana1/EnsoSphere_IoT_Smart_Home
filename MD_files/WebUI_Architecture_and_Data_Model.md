# WebUI – Architecture, Data Model & Feature Flow

## 🧠 Purpose
The WebUI provides a **read-only, real-time visual dashboard** of the smart apartment's current status, including:
- Environment and simulation context
- Device statuses
- Occupants' locations
- Rule activations and sensor outputs

---

## 🌐 Architecture Overview

### Technologies:
- **Frontend**: React + TailwindCSS or Bootstrap
- **Data Source Options**:
  - REST API via backend (recommended)
  - Direct polling to SQLite (read-only client)
- **Polling Frequency**: Every 3–5 seconds (configurable)
- **Entry Point**: `/dashboard`

### Display Philosophy:
- One consistent snapshot per tick (latest `state_id`)
- All views derive from that tick only
- No race conditions due to `processed_by_core = 1` filter

---

## 🧱 Data Sources (Based on `state_id`)

| Source Table      | Used For                             |
|------------------|--------------------------------------|
| `state_raw`      | Environment (weather, season, time)  |
| `sensor_outputs` | Active sensors (e.g., motion, gas)   |
| `rule_triggers`  | Recent rules triggered               |
| `device_states`  | Status of all actuators              |

---

## 🖼️ UI Zones

### 1. 🏡 Environment Bar (Top)
- Current season, time, temperature, weather, is_daytime

### 2. 🧍 Occupants Tracker
- List of current characters and their room (avatar + name)
- Special badge for pets or unknown location

### 3. 🚪 Room Map
- Visual display of all rooms (grid or blueprint)
- Highlight rooms with active sensors or people
- Show device state within room cards

### 4. ⚙️ Device Cards
- Lights, AC, blinds, TV, pet feeder etc.
- Status icons (ON/OFF, numeric values)
- Optional animation (e.g. blinking when just activated)

### 5. 📈 System Events Feed
- List of recent `rule_triggers`
- Rule name, result, timestamp, triggered status
- Optional: collapse by device or room

---

## 🔁 Data Flow
1. Every X seconds → fetch latest `state_id` where `processed_by_core = 1`
2. Query:
   - `SELECT state_json FROM state_raw WHERE id = ?`
   - `SELECT * FROM sensor_outputs WHERE state_id = ?`
   - `SELECT * FROM rule_triggers WHERE state_id = ?`
   - `SELECT * FROM device_states`
3. Format into a `DashboardSnapshot` object
4. Update state in React context/store
5. Rerender all zones with unified data

---

## 📋 Development Tasks

### Phase A: Layout & Skeleton
- [ ] Base layout with React Router and zone placeholders
- [ ] Environment bar + clock display
- [ ] Dummy cards for rooms/devices

### Phase B: Data Client
- [ ] Create `DashboardClient` to fetch state data
- [ ] Integrate polling mechanism (Axios / fetch)
- [ ] Deserialize `state_json` into UI context

### Phase C: Component Wiring
- [ ] Occupants → avatars per room
- [ ] Room map highlights → based on motion/gas
- [ ] Device states → color coded or animated
- [ ] Rule feed → list + icon per rule

### Phase D: Styling & UX Polish
- [ ] Tailwind or Bootstrap integration
- [ ] Icons for weather, seasons, devices
- [ ] Smooth transitions on refresh
- [ ] Support dark/light mode

---

## 📌 Next Steps
- Finalize unified `DashboardSnapshot` format
- Create mock DB or test API endpoints
- Set up dev environment with live DB polling
- Optional: Add toggle for historical `state_id` replay

---

This document outlines the architectural blueprint and visual logic for the smart apartment WebUI, enabling real-time insights into all layers of the simulation system.
