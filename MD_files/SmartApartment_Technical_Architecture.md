# Smart Apartment IoT System – Technical Architecture & Task Breakdown

## 📌 Objective
This document provides a **technical blueprint** and **hands-on task breakdown** for building the Smart Apartment IoT simulation system. It complements the README with more in-depth implementation details, modular design tasks, and developer-focused planning.

---

## 🧱 Core Components Overview

### 1. `Simulator` (Python)
- **Purpose**: Generates `state_json` per tick.
- **Responsibilities**:
  - Simulate: season, time, is_daytime
  - Simulate occupants and their location (routines)
  - Assign weather and temperature conditions
  - Output `state_json` and insert into `state_raw`
- **Technology**:
  - Python 3.x
  - SQLite (via `sqlite3`)
  - Optional: `apscheduler` / `asyncio` for tick management

### 2. `CoreLogic` (Python)
- **Purpose**: Core system logic that handles interpretation and automation
- **Responsibilities**:
  - Pull next unprocessed row from `state_raw`
  - Generate sensor outputs from JSON
  - Evaluate rules and determine actions
  - Publish MQTT messages to relevant devices
  - Update `sensor_outputs`, `rule_triggers`, `device_states`
  - Mark state as processed
  - Internally manage virtual Devices as software modules (not separate containers)
- **Technology**:
  - Python 3.x
  - MQTT via `paho-mqtt`
  - SQLite
  - Modular Rule Engine (JSON-based or Python logic)

### 3. `WebUI` (React)
- **Purpose**: Visual representation of the apartment status
- **Responsibilities**:
  - Poll backend (CoreLogic or DB directly)
  - Display:
    - State (occupants, weather, time)
    - Device states
    - Sensor outputs
    - Rule activity logs
  - Optional: use charts or floorplan for spatial UI
- **Technology**:
  - ReactJS + Tailwind/Bootstrap
  - REST API or direct DB queries (via Python backend)

### 4. `Mosquitto` (MQTT Broker)
- **Purpose**: Message routing backbone
- **Role**: Facilitates publish-subscribe between CoreLogic and (simulated) devices
- **Ports**: 1883 for MQTT (can be exposed in Docker)

### 5. `SQLite` (Database)
- **Purpose**: Shared state and audit log across the system
- **Role**:
  - Source of truth for tick data
  - Prevents data loss between processes
  - Supports replay and analysis

---

## 🔁 Simulation Loop (Per Tick)

1. Simulator creates state_json ➝ inserts into `state_raw`
2. CoreLogic pulls unprocessed state ➝ generates sensors ➝ applies rules ➝ pushes device commands
3. CoreLogic internally simulates device response and state
4. CoreLogic updates DB with `device_states`, `rule_triggers`
5. WebUI pulls only latest processed state_id ➝ presents unified snapshot

---

## 🧩 Data Consistency Principle
- `state_id` (from `state_raw`) is the anchor across all tick-related tables
- Every row in `sensor_outputs`, `rule_triggers` links to one `state_id`
- WebUI relies on `state_id` to fetch consistent data across views

---

## 🔨 Development Tasks Breakdown

### Phase 1: Foundation Setup
- [ ] Docker Compose base with all containers (simulator, corelogic, web, mqtt, db)
- [ ] Initial SQLite schema migrations
- [ ] MQTT broker setup (Mosquitto + exposed port)

### Phase 2: Simulator
- [ ] Environment + time tracking engine
- [ ] Character routines engine (by season)
- [ ] JSON state builder (timestamp, weather, occupants, rooms)
- [ ] Insert to `state_raw`

### Phase 3: CoreLogic
- [ ] DB polling mechanism for unprocessed states
- [ ] SensorManager: convert state to sensor values
- [ ] RuleEngine: evaluate rules and output actions
- [ ] MQTT publisher for actions
- [ ] Log outputs to DB: `sensor_outputs`, `rule_triggers`, `device_states`
- [ ] Internal simulation of device behavior (via device modules)

### Phase 4: WebUI
- [ ] Initial dashboard layout (React)
- [ ] Endpoint or client to query processed state
- [ ] Occupant and environment display
- [ ] Device state cards
- [ ] Live rule activation feed

### Phase 5: Testing & Replay
- [ ] Script for DB cleanup / reset
- [ ] Tool to replay past states (tick by tick)
- [ ] CLI monitor for CoreLogic tick status

---

## 📌 Next Steps
- Define final format for rules and actions (JSON schema)
- Establish naming conventions for sensors/devices
- Create seed simulation scripts for all four seasons
- Build up WebUI visual hierarchy based on rooms and devices

---

This document serves as a starting point for deep technical planning and structured execution of the Smart Apartment system.
Future documents will split off specific components (e.g., `CoreLogic Rule Engine`, `Simulator Character Models`) for deeper focus.
