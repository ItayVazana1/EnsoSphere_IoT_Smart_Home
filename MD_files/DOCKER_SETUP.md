# 🐳 EnsoSphere – Docker Setup Guide

> This document describes how to containerize the entire Smart Apartment IoT simulation system using Docker and Docker Compose.  
It includes example Dockerfiles for each component and a complete `docker-compose.yml`.

---

## 📁 Project Folder Layout (Assumed)

```
EnsoSphere/
├── simulator/
├── corelogic/
├── webui/
├── devices/
├── sensors/
├── data/
├── mqtt/
├── routines/
├── rules/
├── assets/
├── docker/
├── docker-compose.yml
└── .env
```

---

## 🧱 Dockerfile Templates

### 🔹 Python Containers (`simulator`, `corelogic`, etc.)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r corelogic/requirements.txt
ENV PYTHONPATH=/app
CMD ["python", "corelogic/corelogic_main.py"]  # Change per service
```

### 🔹 React WebUI (Simple Serve)

```dockerfile
# Stage 1: Build React app
FROM node:18 as builder
WORKDIR /app
COPY webui/ .
RUN npm install && npm run build

# Stage 2: Serve
FROM node:18-slim
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/build ./build
CMD ["serve", "-s", "build", "-l", "3000"]
```

### 🔹 Mosquitto Broker

Use the official image and mount config:
```yaml
image: eclipse-mosquitto:2.0
volumes:
  - ./mqtt/config:/mosquitto/config
```

---

## 🧩 docker-compose.yml Example

```yaml
version: '3.9'

services:

  simulator:
    build:
      context: .
      dockerfile: docker/Dockerfile.simulator
    container_name: simulator
    environment:
      - PYTHONUNBUFFERED=1
    depends_on:
      - db
      - mqtt
    volumes:
      - .:/app

  corelogic:
    build:
      context: .
      dockerfile: docker/Dockerfile.corelogic
    container_name: corelogic
    environment:
      - PYTHONUNBUFFERED=1
    depends_on:
      - db
      - mqtt
    volumes:
      - .:/app

  webui:
    build:
      context: .
      dockerfile: docker/Dockerfile.webui
    container_name: webui
    ports:
      - "3000:3000"
    depends_on:
      - db

  mqtt:
    image: eclipse-mosquitto:2.0
    container_name: mqtt
    ports:
      - "1883:1883"
    volumes:
      - ./mqtt/config:/mosquitto/config

  db:
    image: nouchka/sqlite3:latest
    container_name: sqlite
    volumes:
      - ./data:/data
```

---

## 📦 .env File (Optional)

```env
TICK_INTERVAL_SIMULATOR=1
TICK_INTERVAL_CORELOGIC=2
DB_PATH=/data/smart_apartment.db
MQTT_BROKER=mqtt
```

---

## 🚀 Running the System

```bash
# From the root of the project:
docker-compose up --build
```

---

## 📌 Tips

- Use `volumes: .:/app` to avoid COPY problems and enable live changes (dev only)
- Consider using `.dockerignore` to skip `__pycache__`, `.git`, and `node_modules`
- Add a `wait-for-it.sh` script or `sleep` delay if services start out of order

---

This guide helps you containerize each service in isolation, while allowing shared access to code, sensors, and devices across containers.
