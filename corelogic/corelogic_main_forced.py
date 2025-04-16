"""
Module: corelogic/corelogic_main_forced.py
Purpose: Forces device commands regardless of conditions, for testing impact on simulator.
Author: Itay Vazana
"""

import os
import time
import random
import mysql.connector
from dotenv import load_dotenv
from corelogic.db_connector import DBConnector
from corelogic.device_manager import DeviceManager
from corelogic.mqtt_publisher import MQTTPublisher

# Load .env variables
load_dotenv()

# DB config
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "db"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "user"),
    "password": os.getenv("MYSQL_PASSWORD", "password"),
    "database": os.getenv("MYSQL_DATABASE", "ensosphere")
}

def wait_for_db():
    print("⏳ Waiting for MySQL to be ready and populated with ticks...")
    for i in range(20):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(id) FROM state_raw;")
            result = cursor.fetchone()
            if result and result[0] is not None:
                print(f"✅ Found latest state_id: {result[0]}")
                return result[0]
            else:
                print(f"⌛ No ticks yet (attempt {i+1}), waiting...")
        except Exception as e:
            print(f"⚠️ DB not ready (attempt {i+1}): {e}")
        time.sleep(2)
    raise RuntimeError("❌ Failed to detect populated DB after 20 attempts")

def main():
    print("\n🧪 Starting CoreLogic Forced Device Manipulation Mode")

    latest_state_id = wait_for_db()

    mqtt_publisher = MQTTPublisher()
    db = DBConnector()
    device_manager = DeviceManager(mqtt_publisher, db)

    test_commands = {
        "air_conditioner_livingroom": {"status": "on", "mode": "cool"},
        "tv_koberoom": {"status": "on"},
        "tv_parentsroom": {"status": "on"},
        "lights_kitchen": {"status": "on"},
        "ventilation_fan_bathroom1": {"status": "on"},
        "pet_door": {"status": "open"},
        "window_livingroom": {"status": "open"},
        "door_lock": {"status": "locked"},
        "audio_system": {"status": "on"},
        "robot_vacuum": {"status": "start_cleaning"},
        "pet_feeder": {"status": "dispense"}
    }

    for i, (device_id, command) in enumerate(test_commands.items(), start=1):
        print(f"\n📦 Forced Command {i}/{len(test_commands)} → {device_id}: {command}")
        device_manager.publish(
            device_id=device_id,
            command=command,
            state_id=latest_state_id,  # Real state ID for DB compatibility
            manual=True
        )
        time.sleep(0.5)

if __name__ == "__main__":
    main()
