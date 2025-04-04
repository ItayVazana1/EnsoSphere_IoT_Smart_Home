# CoreLogic Rule Engine – Internal Design & Execution Flow

## 🧠 Purpose
The Rule Engine is the **automation brain** of the Smart Apartment. It reads the current simulated state, interprets active sensors, and decides which automation rules should be triggered. It then pushes commands to devices via MQTT and logs all activity to the database.

---

## 📦 Core Inputs and Outputs

### 🔹 Inputs
- `state_json` (from `state_raw`): raw simulation snapshot
- `sensor_outputs`: derived sensor statuses per tick
- `rules.json`: list of rules with conditions and actions

### 🔸 Outputs
- MQTT device commands (published)
- Rule evaluation logs → `rule_triggers`
- Final device status → `device_states`

---

## 🧱 Rule Format (JSON Schema)

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
    {"device": "lights_kitchen", "command": {"status": "on"} }
  ]
}
```

### Supported Condition Fields
- `sensor`: references computed sensor values
- `env`: direct keys from `state_json`
- `room_occupied(room_name)`: computed logical sensors (optional)

### Actions
- MQTT commands are built from `device` + `command` JSON

---

## 🔁 Execution Flow

1. **Pull unprocessed `state_raw` row**
2. **Extract environment values from `state_json`**
3. **Compute active sensors** (motion, gas, temp thresholds, etc.)
4. **Evaluate all rules** against environment and sensor values
5. For each triggered rule:
   - Log to `rule_triggers`
   - Publish MQTT command to device topic
   - Update `device_states`
6. Mark `state_raw` row as `processed_by_core = 1`

---

## 🧮 Evaluation Engine (Pseudo Logic)

```python
def evaluate_rule(rule, env, sensors):
    conditions = rule['trigger'].get('all', [])
    for cond in conditions:
        if 'sensor' in cond:
            if sensors.get(cond['sensor']) != cond['equals']:
                return False
        if 'env' in cond:
            if env.get(cond['env']) != cond['equals']:
                return False
    return True
```

---

## 🧪 Rule Engine Tasks

### Phase A: Rule Engine Core
- [ ] Load and cache `rules.json`
- [ ] Define `evaluate_rule()` logic with nested support
- [ ] Implement action dispatcher (MQTT publisher)
- [ ] Log rule activity to `rule_triggers`
- [ ] Integrate with `device_states`

### Phase B: Condition Enrichment
- [ ] Add support for `any`, `not`, `room_occupied()`
- [ ] Threshold-based sensors (e.g., temp > X)
- [ ] Time of day or tick-based logic

### Phase C: Testing
- [ ] Unit tests for rule evaluation logic
- [ ] Load rules and simulate inputs
- [ ] Integration test: simulate state ➝ sensor ➝ rule ➝ command ➝ DB

---

## 📌 Next Step
- Finalize `rules.json` format across all devices
- Build reusable sensor interpreter (for `sensor_outputs`)
- Connect Rule Engine to DB loop inside CoreLogic

---

This document is focused on the inner workings of the Rule Engine and how it connects to sensors, MQTT, and system automation. A future document will define sensor simulation logic and thresholds in detail.
