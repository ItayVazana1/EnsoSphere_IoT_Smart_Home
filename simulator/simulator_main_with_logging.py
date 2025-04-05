
""" 
Module: simulator/simulator_main.py
Purpose: Run simulation loop, generate state_json per tick, store in DB and log outputs.
Author: Itay Vazana
""" 

import time
import json
import os
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv

from simulator.time_manager import TimeManager
from simulator.weather_engine import WeatherEngine
from simulator.occupant_engine import OccupantEngine
from simulator.state_builder import StateBuilder

# Load environment variables
load_dotenv()

# Config
TICK_DELAY = float(os.getenv("TICK_INTERVAL_SIMULATOR", 1))  # in seconds
START_DATETIME = datetime.strptime(os.getenv("SIM_START_DATETIME", "2025-08-01 06:00"), "%Y-%m-%d %H:%M")
SEASON = os.getenv("SIM_SEASON", "Summer")
CHARACTERS = os.getenv("SIM_CHARACTERS", "Testy").split(",")
TICK_BATCH_SIZE = int(os.getenv("TICK_BATCH_SIZE", 1))
MAX_TICKS = os.getenv("MAX_TICKS")
MAX_TICKS = int(MAX_TICKS) if MAX_TICKS and MAX_TICKS.isdigit() else None

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "ensosphere")
}

# Logging setup
LOG_DIR = "sim_log"
os.makedirs(LOG_DIR, exist_ok=True)
RAW_LOG_PATH = os.path.join(LOG_DIR, "full_day_raw_states.txt")
OUTPUT_LOG_PATH = os.path.join(LOG_DIR, "full_day_output.txt")

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
    oe = OccupantEngine(season=SEASON)
    sb = StateBuilder(tm, we, oe)

    # Prepare log files
    raw_log = open(RAW_LOG_PATH, "w", encoding="utf-8")
    output_log = open(OUTPUT_LOG_PATH, "w", encoding="utf-8")

    # Wait for DB to be available
    wait_for_db_connection(DB_CONFIG)

    # Connect to DB
    connection = mysql.connector.connect(**DB_CONFIG)

    total_ticks = 0

    while MAX_TICKS is None or total_ticks < MAX_TICKS:
        for _ in range(TICK_BATCH_SIZE):
            if MAX_TICKS is not None and total_ticks >= MAX_TICKS:
                break

            state = sb.build_state(CHARACTERS)

            # Log raw JSON state
            raw_log.write(json.dumps(state) + "\n")

            # Build log output string
            log_lines = []
            log_lines.append(f"\n📦 Tick @ {state['simulation_time']} → {state['season']}, {state['weather']}, {state['temperature']}°C")
            log_lines.append(f"👥 Occupants: {[o['name'] for o in state['occupants']]}")
            log_lines.append("🧍 Occupant Locations:")
            for occupant in state['occupants']:
                name = occupant['name']
                location = occupant.get('location', 'Unknown')
                log_lines.append(f"  - {name}: {location}")
            log_lines.append(f"🏠 Active Rooms: {state['house_status']['active_rooms']}")
            log_lines.append("📊 Full Room State:")
            for room, data in state["house_status"]["room_state"].items():
                log_lines.append(f"  - {room}: {'Active' if data['active'] else 'Inactive'}")

            # Print and log to file
            for line in log_lines:
                print(line)
                output_log.write(line + "\n")

            store_state_in_db(state, connection)
            tm.advance_tick()
            total_ticks += 1

        print(f"✔ Stored batch of {TICK_BATCH_SIZE} ticks (Total: {total_ticks})")
        output_log.write(f"✔ Stored batch of {TICK_BATCH_SIZE} ticks (Total: {total_ticks})\n")
        time.sleep(TICK_DELAY)

    raw_log.close()
    output_log.close()

if __name__ == "__main__":
    main()
