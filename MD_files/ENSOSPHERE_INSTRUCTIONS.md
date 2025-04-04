# 🧿 EnsoSphere – Project Instructions

Welcome to **EnsoSphere** – a modular smart apartment IoT simulation.  
This document defines the working agreement between the developer (you) and the assistant (me), and outlines how we write, manage, and scale the system.

---

## 🔰 General Principles

1. **📛 Project Identity**
   - Always refer to the project as **EnsoSphere** – no generic names allowed.

2. **🧼 Clarity Over Cleverness**
   - Prioritize readable, clean, and explicit code. Avoid "smart" shortcuts.

3. **🎨 Consistent Style**
   - Python 3.10+, PEP8, `snake_case` for variables/functions, `PascalCase` for classes.
   - React code must be modern, modular, and component-oriented.

4. **🧱 Modular Design**
   - Every component (sensor, device, engine, etc.) must be testable and self-contained.

5. **🧪 Testing is Mandatory**
   - Unit and integration tests are required for every logic unit.
   - Tests must validate DB output, MQTT messages, and full tick cycle.

6. **📝 Proper Documentation**
   - Each file starts with a module docstring.
   - Every function/class must include clear descriptions, args, return types, and side effects.

---

## 🧠 Shared Terminology

- `state_json`: Output of simulator per tick  
- `state_id`: Unique ID for a single tick  
- `tick`: One simulation step  
- `rule_triggers`, `sensor_outputs`, `device_states`: Core tables in the DB

---

## 🔄 System Behavior & Flow

7. **🔁 Tick Synchronization is Sacred**
   - Execution order: `Simulator → CoreLogic → WebUI`
   - DB is the only shared communication layer
   - `processed_by_core` determines readiness for WebUI

8. **🔐 Code Change Discipline**
   - Active logic should not be changed unless instructed. Suggestions only.

9. **📦 Device-Centric Rule Logic**
   - Rules are written per device and inspired by real routine scenarios.
   - Each rule is documented (Excel → JSON) and tested.

10. **⚙️ Smart Additions Only**
    - New sensors/devices must have a clear purpose, MQTT support, and test coverage.

11. **🌍 English-Only Comments**
    - All code/doc comments must be in English. No emojis or slang in code.

---

## 🧰 Infrastructure & Stack

12. **🛠️ Tool Roles**
    - SQLite = sync and storage layer  
    - MQTT = simulated messaging between logic and devices  
    - React WebUI = live visual interface  
    - Docker = container orchestration

13. **🧑‍💻 You Drive – I Support**
    - You define goals and tasks. I help execute with accuracy.

14. **🧭 Keep Context**
    - All work must align with EnsoSphere’s architecture. No hacks, no shortcuts.

---

## 🔍 Advanced Expectations

15. **🗂️ Version Awareness**
    - Track versions of Dockerfiles, libraries, and DB schema when updated.

16. **🧾 .env Ownership**
    - All configuration variables (delays, paths) live in `.env`. Document any addition.

17. **♻️ Reproducibility First**
    - Any scenario must be replayable using `state_id` or season routines.

18. **🚫 No Hidden Logic**
    - All automation goes through the rule engine. No shortcuts in sensor/device logic.

19. **📅 Routine = Reality**
    - Seasonal routines must be realistic. Every 30-min block = narrative + triggers + rules.

20. **🧠 Change Tracking**
    - Log or report every change. Nothing gets added quietly.

21. **🧪 Explicit Test Hooks**
    - Each sensor/device must include a callable test function.

22. **🔌 Tool Integration Clarity**
    - Define purpose and flow for any added external tool (e.g., analytics, visualization).

23. **⚠️ Fail Loudly**
    - Any potential failure (DB, MQTT, logic) must log a clear reason. No silent errors.

24. **📛 Naming Matters**
    - Use intuitive, self-explanatory names for everything. Rename or comment if unclear.

---

Feel free to expand this list as the project evolves. EnsoSphere is a living system – complete, elegant, and evolving.