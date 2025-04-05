"""
Module: simulator/simulator_main.py
Purpose: Run simulation loop, generate state_json per tick, and store in database.
Author: Itay Vazana
"""

import time
import json
import os
import random
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime, timedelta

from simulator.time_manager import TimeManager
from simulator.weather_engine import WeatherEngine
from simulator.occupant_engine import OccupantEngine
from simulator.state_builder import StateBuilder

# Load environment variables
load_dotenv()

# DB config
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "ensosphere")
}

# Tick config
TICK_DELAY = float(os.getenv("TICK_INTERVAL_SIMULATOR", 1))  # seconds
TICK_BATCH_SIZE = int(os.getenv("TICK_BATCH_SIZE", 1))
MAX_TICKS = os.getenv("MAX_TICKS")
MAX_TICKS = int(MAX_TICKS) if MAX_TICKS and MAX_TICKS.isdigit() else None
CHARACTERS = os.getenv("SIM_CHARACTERS", "Testy").split(",")

# Generate or read start datetime
def get_random_start_datetime():
    """Return a random datetime in 2025 at 06:00."""
    year = 2025
    start = datetime(year, 1, 1, 6, 0)
    end = datetime(year, 12, 31, 6, 0)
    return start + timedelta(days=random.randint(0, (end - start).days))


start_datetime_str = os.getenv("SIM_START_DATETIME")
if start_datetime_str:
    START_DATETIME = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
else:
    START_DATETIME = get_random_start_datetime()
    print(f"🎲 Random START_DATETIME selected: {START_DATETIME}")

# Determine season from start date
tm_temp = TimeManager(start_datetime=START_DATETIME)
SEASON = tm_temp.get_season()
print(f"📆 Season determined from date: {SEASON}")

def wait_for_db_connection(config, retries=10, delay=2):
    for attempt in range(retries):
        try:
            print(f"⏳ Attempting DB connection... ({attempt+1}/{retries})")
            conn = mysql.connector.connect(**config)
            conn.close()
            print("✅ Database is up!")
            return
        except mysql.connector.Error:
            print("❌ DB not ready, retrying...")
            time.sleep(delay)
    raise RuntimeError("🛑 Could not connect to DB after multiple retries.")

def store_state_in_db(state: dict, connection) -> None:
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO state_raw (timestamp, simulation_time, season, is_daytime, temperature, weather, state_json)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        state["timestamp"],
        state["simulation_time"],
        state["season"],
        state["is_daytime"],
        state["temperature"],
        state["weather"],
        json.dumps(state)
    ))
    connection.commit()
    cursor.close()

def main():
    print("🚀 Starting simulation...")

    # Init engines
    tm = TimeManager(start_datetime=START_DATETIME)
    we = WeatherEngine()
    oe = OccupantEngine()  # season will be handled dynamically
    sb = StateBuilder(tm, we, oe)

    wait_for_db_connection(DB_CONFIG)
    connection = mysql.connector.connect(**DB_CONFIG)

    total_ticks = 0

    while MAX_TICKS is None or total_ticks < MAX_TICKS:
        for _ in range(TICK_BATCH_SIZE):
            if MAX_TICKS is not None and total_ticks >= MAX_TICKS:
                break

            state = sb.build_state(CHARACTERS)
            print(f"\n📦 Tick @ {state['simulation_time']} → {state['season']}, {state['weather']}, {state['temperature']}°C")
            print(f"👥 Occupants: {[o['name'] for o in state['occupants']]}")
            print("🧍 Occupant Locations:")
            for o in state['occupants']:
                print(f"  - {o['name']}: {o.get('location', 'Unknown')}")
            print(f"🏠 Active Rooms: {state['house_status']['active_rooms']}")
            print("📊 Full Room State:")
            for room, data in state["house_status"]["room_state"].items():
                print(f"  - {room}: {'Active' if data['active'] else 'Inactive'}")

            store_state_in_db(state, connection)
            tm.advance_tick()
            total_ticks += 1

        print(f"✔ Stored batch of {TICK_BATCH_SIZE} ticks (Total: {total_ticks})")
        time.sleep(TICK_DELAY)


if __name__ == "__main__":
    main()
