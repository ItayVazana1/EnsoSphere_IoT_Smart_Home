
# Smart Apartment - Full Room and Device Identity Report

This document contains a full analysis of all rooms, actuators, and sensors within the smart apartment system.  
Each section includes detailed explanations and connectivity notes, followed by a summarized table with checkboxes and overall counts.

---

## Room Profiles

### Entrance

**Actuators:**

- Doorbell
- Door Lock
- Security System
- Motion Detector

**Sensors:**

- Door Sensor (Entrance)
- Internal Scheduler
- Knock Sensor (Door)
- Motion Sensor (Entrance)

---

### Kitchen

**Actuators:**

- Gas Sensor
- Motion Detector
- Pet Feeder

**Sensors:**

- Internal Scheduler
- Motion Sensor (Kitchen)

---

### Entire Home

**Actuators:**

- Security System
- Robot Vacuum

**Sensors:**

- Internal Scheduler

---

### Living Room

**Actuators:**

- Music System
- Blinds
- Lights
- Motion Detector
- Noise Sensor

**Sensors:**

- Internal Scheduler
- Light Sensor (Living Room)
- Motion Sensor (Living Room)
- Noise Sensor (Living Room)

---

### Kids Room

**Actuators:**

- Motion Detector

**Sensors:**

- Motion Sensor (Kids Room)

---

### Hallway

**Actuators:**

- Motion Detector
- Lights

**Sensors:**

- Internal Scheduler
- Motion Sensor (Hallway)

---

### Central System

**Actuators:**

- System Monitor

**Sensors:**

- Internal Scheduler

---

### All Rooms

**Actuators:**

- Window Sensor
- Air Conditioner
- Blinds
- Lights
- Motion Detector
- Windows

**Sensors:**

- Motion Sensors (All Rooms)
- Weather Sensor (Outdoor)
- Temperature Sensor (Indoor)
- Temperature Sensor (Outdoor)
- Light Sensor (Outdoor)
- Internal Scheduler

---

### Balcony

**Actuators:**

- Blinds
- Motion Detector

**Sensors:**

- Motion Sensor (Balcony)
- Weather Sensor (Outdoor)

---

### Outdoor

**Actuators:**

- Weather Station
- Temperature Sensor

**Sensors:**

- Temperature Sensor (Outdoor)
- Weather Sensor (Outdoor)

---

### Bathroom

**Actuators:**

- Ventilation Fan

**Sensors:**

- Humidity Sensor (Bathroom)

---

### Bedroom

**Actuators:**

- Windows
- Window Actuator

**Sensors:**

- Weather Sensor (Outdoor)

---


## Room Device & Sensor Summary

| Room | Actuator: Lights | Actuator: Blinds | Actuator: Air Conditioner | Actuator: Robot Vacuum | Actuator: Security System | Sensor: Motion Sensor | Sensor: Temperature Sensor | Sensor: Light Sensor | Sensor: Humidity Sensor | Sensor: Weather Sensor |
|---|---|---|---|---|---|---|---|---|---|---|
| Entrance | | | | | ✔️ | ✔️ | | | | |
| Kitchen | | | | | | ✔️ | | | | |
| Entire Home | | | | ✔️ | ✔️ | | | | | |
| Living Room | ✔️ | ✔️ | | | | ✔️ | | ✔️ | | |
| Kids Room | | | | | | ✔️ | | | | |
| Hallway | ✔️ | | | | | ✔️ | | | | |
| Central System | | | | | | | | | | |
| All Rooms | ✔️ | ✔️ | ✔️ | | | ✔️ | ✔️ | ✔️ | | ✔️ |
| Balcony | | ✔️ | | | | ✔️ | | | | ✔️ |
| Outdoor | | | | | | | ✔️ | | | ✔️ |
| Bathroom | | | | | | | | | ✔️ | |
| Bedroom | | | | | | | | | | ✔️ |

## Total Device and Sensor Count

| Category | Total Count |
|---|---|
| Total Actuators in Home | 31 |
| Total Sensors in Home | 27 |

