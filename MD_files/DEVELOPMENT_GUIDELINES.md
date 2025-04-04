# 🛠️ EnsoSphere – Development Guidelines

> Unified principles for writing clean, maintainable, and testable code across all system components.

---

## 📦 Folder & File Structure

- Follow modular separation:
  - `simulator/` → Time, environment, and occupant logic
  - `corelogic/` → Sensors, rule engine, MQTT dispatcher, and device management
  - `webui/` → React frontend
  - `data/` → SQLite and logs
  - `rules/` → JSON automation rules
  - `routines/` → Seasonal Excel-based schedules
  - `docs/` → All planning and documentation
- Place all helper scripts inside `utils/` or co-located `helpers.py`

---

## 🧠 Before You Code

- Clearly define the **purpose** of each module before starting
- Write a **design plan** or bullet list with:
  - Inputs & outputs
  - External dependencies (DB, MQTT, API)
  - Logic phases or flow steps
- Consider side-effects (DB writes, file I/O, MQTT messages)
- Reuse existing utilities where possible
- Start with small **isolated testable units**

---

## 🧱 Code Standards

- Use **Python 3.10+** syntax (match project version)
- Follow **PEP8** and naming conventions:
  - `snake_case` for functions & variables
  - `PascalCase` for class names
  - Avoid abbreviations (e.g., `room_name`, not `rm`)
- Add docstrings to all public functions and classes
- Prefer **explicit logic** over clever tricks
- Always check if `state_id` is consistent when interacting with DB

---

## 🧪 Testing Guidelines

- Every file must include a corresponding `test_<module>.py`
- Write:
  - Unit tests (per function or logic block)
  - Integration tests (e.g., DB + rule engine + device response)
- Use mock states (`state_json`) from `examples/` or `routines/`
- Validate:
  - DB writes
  - MQTT messages
  - Rule triggers
  - Device state updates (simulated and logged)

---

## 🔄 Rule, Sensor & Device Development

- Define rules in `rules.json` with:
  - Clear trigger conditions
  - Explicit device actions
- Keep sensor logic **deterministic** and transparent
- CoreLogic manages all device modules internally:
  - Simulates device behavior
  - Publishes MQTT commands
  - Updates `device_states` table
- Before adding new sensors/devices:
  - Implement MQTT integration
  - Extend sensor and device manager modules
  - Write validation tests

---

## 🖥 WebUI Best Practices

- Pull data only from `processed_by_core = 1` state snapshots
- Keep rendering logic separate from data-fetching
- Store full `DashboardSnapshot` state in React context/store
- Prefer polling via `DashboardClient`, not direct SQL calls in UI

---

## 🔐 Database & Timing

- Never update a `state_raw` row except to mark `processed_by_core = 1`
- Use `state_id` as the atomic identifier for all sensor, rule, and device updates
- Maintain tick order integrity (no skipping ticks)
- Use CLI replay tools for testing rules or debugging

---

## 📋 Documentation Expectations

- Every file must start with:
  \"\"\"python
  Module: corelogic/devices.py
  Purpose: Handle internal logic for actuator simulation and MQTT dispatch
  Author: Itay Vazana
  \"\"\"
- Every function should include:
  - What it does
  - Arguments & return types
  - Side effects (DB, MQTT, etc.)

---

## 📌 Final Checklist Before Merge

- [ ] Is the logic unit-tested?
- [ ] Does the rule have test data?
- [ ] Does the module write to the right tables?
- [ ] Are simulated devices correctly responding to commands?
- [ ] Is MQTT tested end-to-end?
- [ ] Did you update related documentation?
- [ ] Did you use meaningful names and comments?

---

This file is a live guide. Update it whenever major practices evolve or new standards are introduced.
