"""
Module: corelogic/corelogic_main.py
Purpose: Debug mode – toggles device states and writes to DB; includes diagnostics to detect unprocessed tick issues.
Author: Itay Vazana
"""

import time
import json
import random
import os
import mysql.connector
from dotenv import load_dotenv
import socket
from datetime import datetime

# --- Retry configuration ---
MAX_TICK_RETRIES = 5
TICK_RETRY_DELAY = 5  # seconds

# Load environment variables
load_dotenv()

# Console output toggle
CONCISE_MODE = os.getenv("CORE_LOGIC_CONCISE_MODE", "False").lower() in ("1", "true", "yes")

# Environment vars
DEVICE_MAP_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "device_room_map.json")
MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DB = os.getenv("MYSQL_DATABASE", "ensosphere")
MYSQL_USER = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")

def wait_for_mysql(host: str, port: int, timeout: int = 60):
    print(f"\n⏳ Waiting for MySQL at {host}:{port} ...")
    start = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=5):
                print(f"🔗 Connected to MySQL @ {host}:{port} | DB: {MYSQL_DB} | USER: {MYSQL_USER}")
                print("✅ MySQL is available!")
                return
        except (socket.timeout, ConnectionRefusedError):
            if time.time() - start > timeout:
                raise TimeoutError(f"MySQL not available after {timeout} seconds.")
            time.sleep(1)

def load_device_map() -> dict:
    print("📥 Loading device map...")
    with open(DEVICE_MAP_PATH, "r", encoding="utf-8") as f:
        full_map = json.load(f)
        flat_map = {dev["id"]: {"type": dev["type"], "room": room}
                    for room, devs in full_map.items() for dev in devs}
        print(f"✅ Loaded {len(flat_map)} devices from map.")
        return flat_map

def parse_device_type(device_type: str) -> str:
    names = {
        "air_conditioner": "Air Conditioner",
        "ventilation_fan": "Ventilation Fan",
        "audio_system": "Audio System",
        "tv": "Television",
        "window": "Window",
        "blinds": "Blinds",
        "robot_vacuum": "Robot Vacuum",
        "lights": "Lights",
        "door_lock": "Main Door Lock",
        "pet_door": "Pet Door",
        "pet_feeder": "Pet Feeder",
        "security_system": "Security System"
    }
    return names.get(device_type, device_type.capitalize())

def get_next_unprocessed_state(conn):
    try:
        print("🔍 Checking for unprocessed ticks...")
        cursor = conn.cursor()

        cursor.execute("SELECT id, processed_by_core, processed_at FROM state_raw ORDER BY id DESC LIMIT 5")
        for row in cursor.fetchall():
            print(f"  [DEBUG] Tick ID={row[0]} → processed_by_core={row[1]}, processed_at={row[2]}")

        cursor.execute("SELECT id, state_json FROM state_raw WHERE processed_by_core = 0 ORDER BY id ASC LIMIT 1")
        row = cursor.fetchone()
        cursor.close()
        if row:
            print(f"🟢 Found unprocessed tick: ID {row[0]}")
            return {"state_id": row[0], "state_json": json.loads(row[1])}
        else:
            print("🟡 No unprocessed tick found.")
    except Exception as e:
        print(f"❌ Error fetching tick: {e}")
    return None

def mark_state_as_processed(conn, state_id):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE state_raw SET processed_by_core = 1, processed_at = %s WHERE id = %s",
            (datetime.now(), state_id)
        )
        conn.commit()
        cursor.close()
        print(f"📝 Marked tick {state_id} as processed.")
    except Exception as e:
        print(f"❌ Failed to mark tick {state_id} as processed: {e}")

def reconnect_if_needed(conn):
    try:
        conn.ping(reconnect=True, attempts=3, delay=2)
    except Exception as e:
        print(f"🔌 Reconnecting to DB due to error: {e}")
        return mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
    return conn

def wait_for_first_tick(conn, max_wait=60):
    print("⏳ Waiting for first tick from simulator...")
    start = time.time()
    cursor = conn.cursor()
    while time.time() - start < max_wait:
        cursor.execute("SELECT COUNT(*) FROM state_raw")
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"✅ Found {count} ticks in DB. Starting processing loop.")
            return
        time.sleep(1)
    raise RuntimeError("⛔ No ticks found in DB after waiting.")



if __name__ == "__main__":
    print("\n🧪 CoreLogic DEBUG MODE – randomly toggling device states for simulator testing (MySQL).\n")

    wait_for_mysql(MYSQL_HOST, MYSQL_PORT)

    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        autocommit=True  # ✅ Ensures visibility of new simulator ticks
    )

    wait_for_first_tick(conn)
    device_map = load_device_map()
    consecutive_empty_ticks = 0

    while True:
        try:
            conn = reconnect_if_needed(conn)
            state = get_next_unprocessed_state(conn)

            if state:
                consecutive_empty_ticks = 0
                state_id = state['state_id']
                all_device_ids = list(device_map.keys())
                selected_devices = random.sample(all_device_ids, k=min(len(all_device_ids), random.randint(2, 4)))
                actions = []

                for dev_id in selected_devices:
                    new_status = random.choice(["on", "off"])
                    meta = device_map[dev_id]
                    room = meta.get("room", "Unknown")
                    device_type = parse_device_type(meta.get("type", "Unknown"))
                    actions.append({"device_id": dev_id, "command": {"status": new_status}})
                    if not CONCISE_MODE:
                        print(f"⚙️ {device_type} in {room}: {dev_id} → {new_status}")

                now = datetime.now()
                cursor = conn.cursor()

                for action in actions:
                    cursor.execute("""
                        INSERT INTO device_actions (state_id, device_id, command_json, executed_at)
                        VALUES (%s, %s, %s, %s)
                    """, (state_id, action["device_id"], json.dumps(action["command"]), now))

                for action in actions:
                    cursor.execute("""
                        INSERT INTO device_states (device_id, state_json, last_updated)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE state_json = VALUES(state_json), last_updated = VALUES(last_updated)
                    """, (action["device_id"], json.dumps(action["command"]), now))

                conn.commit()
                cursor.close()
                mark_state_as_processed(conn, state_id)

                if CONCISE_MODE:
                    changes_str = ", ".join(f"{a['device_id']} → {a['command']['status']}" for a in actions)
                    print(f"🌀 Tick {state_id} → Devices changed: {changes_str}")
                else:
                    print(f"✔️ Tick {state_id} processed with {len(actions)} device changes.")

            else:
                consecutive_empty_ticks += 1
                print(f"⏳ Sleeping {TICK_RETRY_DELAY}s... (attempt {consecutive_empty_ticks}/{MAX_TICK_RETRIES})")
                time.sleep(TICK_RETRY_DELAY)

                if consecutive_empty_ticks >= MAX_TICK_RETRIES:
                    raise RuntimeError("Too many attempts without finding a tick. Shutting down CoreLogic.")

        except Exception as e:
            import traceback
            print(f"\n❌ Error during CoreLogic loop: {e}")
            traceback.print_exc()
            break
