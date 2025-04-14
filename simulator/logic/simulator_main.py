"""
Module: simulator/simulator_main.py
Purpose: Run simulation loop using World + House + DB + MQTT. Fully modular and encapsulated.
Author: Itay Vazana
"""

import time
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

from simulator.engines.time_manager import TimeManager
from simulator.engines.weather_engine import WeatherEngine
from simulator.core.world import World
from simulator.core.house import House
from simulator.infra.infrastructure import Infrastructure
from simulator.infra.db_connector import DBConnector
from simulator.logic.state_builder import StateBuilder
from sensors.sensors_registry import get_sensors_by_room

# Load environment variables
load_dotenv()

# Character & timing config
CHARACTERS = os.getenv("SIM_CHARACTERS", "Testy").split(",")
TICK_DELAY = float(os.getenv("TICK_INTERVAL_SIMULATOR", 1))
TICK_BATCH_SIZE = int(os.getenv("TICK_BATCH_SIZE", 1))
MAX_TICKS = os.getenv("MAX_TICKS")
MAX_TICKS = int(MAX_TICKS) if MAX_TICKS and MAX_TICKS.isdigit() else None
CONCISE_MODE = os.getenv("SIMULATOR_CONCISE_MODE", "False").lower() in ("1", "true", "yes")

# Start date config
def get_random_start_datetime():
    year = 2025
    start = datetime(year, 1, 1, 6, 0)
    end = datetime(year, 12, 31, 6, 0)
    return start + timedelta(days=random.randint(0, (end - start).days))

start_datetime_str = os.getenv("SIM_START_DATETIME")
START_DATETIME = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M") if start_datetime_str else get_random_start_datetime()
print(f"📆 START_DATETIME: {START_DATETIME}")

# Initialize core modules
time_manager = TimeManager(START_DATETIME)
weather_engine = WeatherEngine()
world = World(time_manager, weather_engine)

sensor_map = get_sensors_by_room()
house = House(sensor_map)

infra = Infrastructure()
publisher = infra.publisher  # Only one publisher instance in the system

builder = StateBuilder(world, house, publisher)
db = DBConnector()

# Connect to services
db.wait_for_db()
db.connect()

# Output helper
def print_concise(state, previous):
    print(f"\n📦 Tick @ {state['simulation_time']} → {state['season']}, {state['weather']}, {state['temperature']}°C")
    occ = " | ".join(f"{o['name']} → {o.get('location', 'Unknown')}" for o in state['occupants'])
    print(f"🧍 Occupants: {occ}")
    changes = [
        (sid, previous['sensors'].get(sid) if previous else None, val)
        for sid, val in state["sensors"].items()
        if previous is None or val != previous["sensors"].get(sid)
    ]
    if changes:
        print("🛰️ Sensor Changes:")
        for sid, old, new in changes:
            print(f"  - {sid}: {old} → {new}")
    else:
        print("🛰️ No sensor changes from last tick.")

# Simulation loop
def main():
    print("🚀 Simulation Started")
    total_ticks = 0
    previous_state = None

    try:
        while MAX_TICKS is None or total_ticks < MAX_TICKS:
            for _ in range(TICK_BATCH_SIZE):
                if MAX_TICKS and total_ticks >= MAX_TICKS:
                    break

                world.advance()
                device_states = infra.get_device_states()
                state = builder.build_state(CHARACTERS, device_states)
                db.insert_state(state)
                infra.publish_sensors(state["sensors"])

                if CONCISE_MODE:
                    print_concise(state, previous_state)
                else:
                    print(f"\n📦 Tick @ {state['simulation_time']} → {state['season']}, {state['weather']}, {state['temperature']}°C")
                    print(f"👥 Occupants: {[o['name'] for o in state['occupants']]}")
                    print("🧍 Locations:")
                    for o in state['occupants']:
                        print(f"  - {o['name']}: {o.get('location', 'Unknown')}")
                    print("🏠 Active Rooms:", state["house_status"]["active_rooms"])
                    print("🛰️ All Sensors:")
                    for sid, value in state["sensors"].items():
                        print(f"  - {sid}: {value}")

                previous_state = state
                total_ticks += 1

            print(f"✔ Batch of {TICK_BATCH_SIZE} ticks (Total: {total_ticks})")
            time.sleep(TICK_DELAY)

    finally:
        infra.shutdown()
        print("🛑 Simulation shutdown complete.")


if __name__ == "__main__":
    main()
