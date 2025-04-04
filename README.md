# 🧿 EnsoSphere - Smart Apartment IoT Simulation (Dockerized Architecture)

> *“A circle has no beginning or end. Like time. Like energy. Like a home that breathes and responds.”*  
> *Inspired by the Zen concept of Ensō (円相), symbolizing harmony, completeness, and simplicity in complexity.*

![Smart Apartment Cover](assets/Final_Cover.PNG)

---

Welcome to **EnsoSphere** – a fully modular, database-driven smart apartment IoT system simulation.  
This version reflects the **Dockerized and containerized** architecture, starting from **Phase 1 onward**.

---

> 🗃️ **Looking for the original non-Docker version?**  
> It has been preserved inside the `/archive/` folder for historical reference.  
> You can explore the legacy design, SQLite structure, and simulation logic from the original standalone version.

---

## 📌 Project Phases

### ✅ Phase 1: Bootstrap Infrastructure
- Set up Docker containers for: `simulator`, `corelogic`, `webui`, `mqtt`, `mysql`, `adminer`
- Configure `.env`, volumes, and `docker-compose.yml`
- Test connections to MQTT and MySQL
- Confirm WebUI and Adminer run correctly

### 🛠 Phase 2 and beyond
- Build simulator time engine (`time_manager.py`)
- Construct dynamic `state_json` per tick
- Insert state into DB and process it via CoreLogic
- Trigger rules and control devices with MQTT

---

## 🧱 System Architecture – Core Containers

| Container       | Role                                               |
|----------------|----------------------------------------------------|
| `simulator`     | Generates `state_json` ticks (occupants, weather) |
| `corelogic`     | Sensor → Rule → Device engine (with MQTT output) |
| `webui`         | React dashboard to visualize current state        |
| `mosquitto`     | MQTT broker for device messaging                  |
| `mysql`         | System database and tick-based state repository  |
| `adminer`       | Browser-based MySQL viewer                        |

---

## 📦 Archived Folder

```bash
/archive/   <-- Contains the original standalone version (pre-Docker)
```

---

## 📦 Component Inventory
(unchanged - sensors, devices, etc.)

---

## 🔧 Technologies Used

| Category       | Library/Tool        |
|----------------|---------------------|
| Language       | Python 3.x, JavaScript (React) |
| Messaging      | MQTT (`paho-mqtt`, Mosquitto)  |
| Database       | MySQL (via Docker)             |
| Time Engine    | Accelerated custom time engine |
| Web Frontend   | React + Tailwind or Bootstrap  |
| Scheduler      | `apscheduler`, `asyncio`       |

---

## 📂 Folder Structure

```bash
EnsoSphere/
├── archive/             # Original non-Docker codebase
├── simulator/           # Simulator engine (Docker-based)
├── corelogic/           # Core logic & rule engine
├── webui/               # React frontend
├── mqtt/                # Mosquitto config
├── tests/               # Infra/unit tests
├── docker/              # Dockerfiles
├── docker-compose.yml   # Orchestration config
└── .env                 # Environment variables
```

---

## 🧪 Bootstrap Test

To verify that Docker infra is healthy:
```bash
docker-compose up -d --build
docker exec -it simulator bash
python tests/test_bootstrap_phase1.py
```

---

## 👨‍💻 Created by: Itay Vazana

[GitHub Profile](https://github.com/ItayVazana1)  
[LinkedIn](https://www.linkedin.com/in/itayvazana)

---

## 🌀 Why "EnsoSphere"?
Ensō (円相) in Zen art is a circle drawn in a single breath — symbolizing perfection, fluidity, and interdependence.  
This project reflects that vision: a living, breathing system. Complete, yet dynamic.

---