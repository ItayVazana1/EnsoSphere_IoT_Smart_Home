# SQLite – Structure, Access Patterns & Ownership

## 🧠 Purpose
SQLite is the **single source of truth** for the Smart Apartment simulation. It coordinates data flow across all containers and provides a consistent, queryable snapshot of the system per tick.

---

## 🧱 Core Database Tables (Schemas)

### 1. `state_raw`
Holds the full simulation snapshot per tick (written by `Simulator`).
```sql
CREATE TABLE state_raw (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  simulation_time TEXT NOT NULL,
  state_json TEXT NOT NULL,
  processed_by_core INTEGER DEFAULT 0,
  processed_at TEXT
);
```

### 2. `sensor_outputs`
Derived sensor values from `state_json` (written by `CoreLogic`).
```sql
CREATE TABLE sensor_outputs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  state_id INTEGER,
  sensor_id TEXT,
  value TEXT,
  evaluated_at TEXT
);
```

### 3. `rule_triggers`
Rule evaluation results (written by `CoreLogic`).
```sql
CREATE TABLE rule_triggers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  state_id INTEGER,
  rule_id TEXT,
  triggered INTEGER,
  conditions_json TEXT,
  actions_json TEXT,
  evaluated_at TEXT
);
```

### 4. `device_states`
Latest state of each device (updated by `CoreLogic`).
```sql
CREATE TABLE device_states (
  device_id TEXT PRIMARY KEY,
  state_json TEXT,
  last_updated TEXT
);
```

---

## 🔁 Write & Read Responsibilities

| Table           | Writer        | Readers                 |
|----------------|---------------|--------------------------|
| `state_raw`     | Simulator      | CoreLogic, WebUI         |
| `sensor_outputs`| CoreLogic      | WebUI                    |
| `rule_triggers` | CoreLogic      | WebUI                    |
| `device_states` | CoreLogic      | WebUI                    |

---

## 🔄 Access Patterns

### 🖋️ INSERTs
- `Simulator` inserts into `state_raw` once per tick
- `CoreLogic` inserts into `sensor_outputs`, `rule_triggers`
- `CoreLogic` **upserts** into `device_states`

### 📥 SELECTs
- `CoreLogic` pulls from `state_raw WHERE processed_by_core = 0`
- `WebUI` pulls:
  - Latest `state_id` where `processed_by_core = 1`
  - Full `state_json` from `state_raw`
  - Related `sensor_outputs`, `rule_triggers`
  - Current `device_states`

### ✅ UPDATEs
- `CoreLogic` sets `processed_by_core = 1` and logs `processed_at`
- `device_states` is overwritten per device

---

## 🧪 Query Examples

### Get latest processed tick
```sql
SELECT id FROM state_raw WHERE processed_by_core = 1 ORDER BY id DESC LIMIT 1;
```

### Pull data for rendering UI snapshot
```sql
SELECT state_json FROM state_raw WHERE id = ?;
SELECT * FROM sensor_outputs WHERE state_id = ?;
SELECT * FROM rule_triggers WHERE state_id = ?;
SELECT * FROM device_states;
```

### Get next tick to process
```sql
SELECT * FROM state_raw WHERE processed_by_core = 0 ORDER BY id ASC LIMIT 1;
```

---

## 🔐 Concurrency & Locking
- SQLite supports concurrent reads, single-writer.
- Tick loop is serialized: each writer only writes once per tick.
- Enforced access via Python locks or atomic operations.

---

## 🧰 Recommended Tools
- Use `sqlite3` or `SQLAlchemy` for Python interaction
- Use DB browser (e.g., DB Browser for SQLite) for debug
- Expose volume mount for persistent storage in Docker

---

## 🧪 Testing & Replay
- Snapshots can be re-evaluated by reprocessing `state_raw`
- Manual override possible via CLI: `--replay state_id`
- Enables debugging of specific ticks or time ranges

---

## 📌 Next Steps
- Add indexes on `state_id` in all dependent tables
- Define DB migration scripts and seeding helpers
- Implement DB cleanup/reset utility
- Consider logging anomalies to separate `debug_log` table

---

This document defines the data backbone of the Smart Apartment system and how each service interacts with the database in a controlled and structured way.
