# Timing & Synchronization – System Flow & Scheduling Logic

## 🧠 Purpose
This document explains the **timing architecture** and **synchronization model** of the Smart Apartment system, including how simulation ticks, processing, database updates, and UI rendering stay in sync across different containers.

---

## 🔁 High-Level System Flow (per Tick)

1. **Simulator**:
   - Every X seconds, generates a new `state_json`
   - Inserts row into `state_raw` with `processed_by_core = 0`

2. **CoreLogic**:
   - Every Y seconds, checks for next unprocessed tick
   - Pulls from `state_raw`
   - Evaluates sensors → rules → devices
   - Logs results into `sensor_outputs`, `rule_triggers`, `device_states`
   - Updates `processed_by_core = 1`

3. **WebUI**:
   - Every Z seconds, pulls the latest processed tick (`processed_by_core = 1`)
   - Reads and renders data from:
     - `state_raw.state_json`
     - `sensor_outputs`, `rule_triggers`, `device_states`

---

## ⏱️ Suggested Timing Intervals

| Component  | Frequency   | Notes                                 |
|------------|-------------|----------------------------------------|
| Simulator  | Every 1 sec | Generates new simulated world state    |
| CoreLogic  | Every 2 sec | Processes 1 new state per iteration    |
| WebUI      | Every 3 sec | Polls DB for latest processed state    |

> ⚠️ Note: Intervals are configurable and must preserve this priority order:
`Simulator < CoreLogic < WebUI`

---

## 🔄 Flow Synchronization Strategy

### Why not use shared memory or queues?
We use the **DB as a shared buffer** to simplify debugging, inspection, and replay.

### Preventing race conditions:
- WebUI only reads data where `processed_by_core = 1`
- CoreLogic only reads states where `processed_by_core = 0`
- Simulator only writes new states and never touches others

---

## 🧩 Tick ID and Traceability
- `state_id` serves as the **global tick identifier**
- All downstream tables (`sensor_outputs`, `rule_triggers`) link to `state_id`
- Guarantees consistency per tick across all views and queries

---

## 📈 Timeline Example (Simulated Time)

```
[T+0s] Simulator ➝ Insert state_id=101
[T+1s] CoreLogic ➝ Process state_id=101, mark processed_by_core=1
[T+2s] WebUI ➝ Reads state_id=101, renders full snapshot
```

Result: All components remain synchronized even with independent clocks.

---

## ✅ Replay & Debug Modes
- Possible to replay past `state_id` ranges for testing
- CoreLogic supports `--reprocess` mode
- WebUI can support manual time scrubber via `?state_id=123`

---

## 📌 Future Enhancements
- Central timing controller (tick master container)
- Publish current tick over MQTT for observability
- Push-based updates to WebUI (via WebSocket or POST)

---

This timing layer is essential for maintaining a smooth, understandable and replayable simulation system where all containers collaborate loosely but synchronously through well-ordered tick snapshots.
