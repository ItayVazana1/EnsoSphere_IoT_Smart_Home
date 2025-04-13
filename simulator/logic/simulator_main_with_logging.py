"""
Module: simulator/simulator_main.py
Purpose: Run simulation loop, generate state_json per tick, store in DB and log outputs.
Author: Itay Vazana
"""

import time
import json
import os
import random
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime, timedelta

from simulator.engines.time_manager import TimeManager
from simulator.engines.weather_engine import WeatherEngine
from simulator.engines.occupant_engine import OccupantEngine
from simulator.logic.state_builder import StateBuilder
from simulator.infra.device_state_fetcher import fetch_device_states

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
TICK_DELAY = float(os.getenv("TICK_INTERVAL_SIMULATOR", 1))
TICK_BATCH_SIZE = int(os.getenv("TICK_BATCH_SIZE", 1))
MAX_TICKS = os.getenv("MAX_TICKS")
MAX_TICKS = int(MAX_TICKS) if MAX_TICKS and MAX_TICKS.isdigit() else None
CHARACTERS = os.getenv("SIM_CHARACTERS", "Testy").split(",")

# Console output mode
CONCISE_MODE = os.getenv("SIMULATOR_CONCISE_MODE", "False").lower() in ("1", "true", "yes")

# Logging setup
LOG_DIR = "sim_log"
os.makedirs(LOG_DIR, exist_ok=True)
RAW_LOG_PATH = os.path.join(LOG_DIR, "full_day_raw_states.txt")
OUTPUT_LOG_PATH = os.path.join(LOG_DIR, "full_day_output.txt")

# Generate or read start datetime
def get_random_start_datetime():
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

# Precompute season
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
    INSERT INTO state_raw (
        timestamp,
        simulation_time,
        season,
        is_daytime,
        temperature,
        weather,
        state_json,
        processed_by_core
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        state["timestamp"],
        state["simulation_time"],
        state["season"],
        state["is_daytime"],
        state["temperature"],
        state["weather"],
        json.dumps(state),
        False
    ))
    connection.commit()
    cursor.close()

def print_and_log(line: str, output_log):
    print(line)
    output_log.write(line + "\n")

def main():
    print("🚀 Starting simulation...")

    tm = TimeManager(start_datetime=START_DATETIME)
    we = WeatherEngine()
    oe = OccupantEngine()
    sb = StateBuilder(tm, we, oe)

    wait_for_db_connection(DB_CONFIG)
    connection = mysql.connector.connect(**DB_CONFIG)

    # Prepare logs
    raw_log = open(RAW_LOG_PATH, "w", encoding="utf-8")
    output_log = open(OUTPUT_LOG_PATH, "w", encoding="utf-8")

    total_ticks = 0
    previous_state = None

    while MAX_TICKS is None or total_ticks < MAX_TICKS:
        for _ in range(TICK_BATCH_SIZE):
            if MAX_TICKS is not None and total_ticks >= MAX_TICKS:
                break

            device_states = fetch_device_states()
            state = sb.build_state(CHARACTERS, device_states)

            raw_log.write(json.dumps(state) + "\n")

            log_lines = []
            log_lines.append(f"\n📦 Tick @ {state['simulation_time']} → {state['season']}, {state['weather']}, {state['temperature']}°C")
            occupants_str = " | ".join(f"{o['name']} → {o.get('location', 'Unknown')}" for o in state['occupants'])
            log_lines.append(f"🧍 Occupants: {occupants_str}")

            changed_sensors = []
            for sid, val in state['sensors'].items():
                prev_val = previous_state.get("sensors", {}).get(sid) if previous_state else None
                if val != prev_val:
                    changed_sensors.append((sid, prev_val, val))

            if changed_sensors:
                log_lines.append("🛰️ Sensor Changes:")
                for sid, old, new in changed_sensors:
                    log_lines.append(f"  - {sid}: {old} → {new}")
            else:
                log_lines.append("🛰️ No sensor changes from last tick.")

            log_lines.append(f"🏠 Active Rooms: {state['house_status']['active_rooms']}")
            log_lines.append("📊 Full Room State:")
            for room, data in state["house_status"]["room_state"].items():
                log_lines.append(f"  - {room}: {'Active' if data['active'] else 'Inactive'}")

            for line in log_lines:
                print_and_log(line, output_log)

            store_state_in_db(state, connection)
            tm.advance_tick()
            total_ticks += 1
            previous_state = state

        print_and_log(f"✔ Stored batch of {TICK_BATCH_SIZE} ticks (Total: {total_ticks})", output_log)
        time.sleep(TICK_DELAY)

    raw_log.close()
    output_log.close()

if __name__ == "__main__":
    main()
