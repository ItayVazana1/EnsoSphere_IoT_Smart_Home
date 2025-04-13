"""
Module: simulator/device_state_fetcher.py
Purpose: Fetch latest known device states from MySQL to be used in environmental simulation.
Author: Itay Vazana
"""

import mysql.connector
import json
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "ensosphere")
}

def fetch_device_states() -> Dict[str, dict]:
    """
    Fetch the latest state of all devices from the device_states table.

    Returns:
        dict: {device_id: state_dict, ...}
    """
    device_states = {}

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT device_id, state_json FROM device_states")

        for device_id, state_json in cursor.fetchall():
            try:
                state = json.loads(state_json)
                device_states[device_id] = state
            except json.JSONDecodeError:
                print(f"⚠️ Could not parse state for device: {device_id}")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ MySQL error in fetch_device_states: {err}")

    return device_states


if __name__ == "__main__":
    result = fetch_device_states()
    print(f"Total device states fetched: {len(result)}")
    for k, v in result.items():
        print(f"{k} → {v}")
