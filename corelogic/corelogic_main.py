"""
Module: corelogic/corelogic_main.py
Purpose: Main tick processor – evaluates sensor-based rules and triggers device actions.
Author: Itay Vazana
"""

import time
import os
from dotenv import load_dotenv
from corelogic.db_connector import DBConnector
from corelogic.rules_loader import load_all_rules
from corelogic.rule_engine import RuleEngine
from corelogic.mqtt_sensor_listener import MQTTSensorListener
from corelogic.mqtt_publisher import MQTTPublisher
from corelogic.device_manager import DeviceManager
import mysql.connector

# Load environment variables
load_dotenv()
TICK_INTERVAL = float(os.getenv("TICK_INTERVAL_CORELOGIC", 5.0))
CONCISE_MODE = os.getenv("CORE_LOGIC_CONCISE_MODE", "False").lower() in ("1", "true", "yes")


def main():
    print("\n🚀 Starting CoreLogic Engine (Tick-Based Rule Processor)")

    # Wait for DB to be ready
    max_retries = 10
    for attempt in range(1, max_retries + 1):
        try:
            print(f"⏳ Attempting DB connection... ({attempt}/{max_retries})")
            db_connection = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST", "db"),
                port=int(os.getenv("MYSQL_PORT", 3306)),
                user=os.getenv("MYSQL_USER", "user"),
                password=os.getenv("MYSQL_PASSWORD", "password"),
                database=os.getenv("MYSQL_DATABASE", "ensosphere"),
                autocommit=True
                # Ensure MySQL connection is autocommit-enabled
            )
            print("✅ Database is up!")
            break
        except mysql.connector.Error as e:
            print(f"❌ DB connection failed: {e}")
            time.sleep(3)
    else:
        print("❌ Could not connect to DB after multiple attempts. Exiting.")
        return

    # Initialize infrastructure components
    db = DBConnector()
    mqtt_listener = MQTTSensorListener()
    mqtt_listener.start()
    mqtt_publisher = MQTTPublisher()
    device_manager = DeviceManager(mqtt_publisher, db)

    # Load rules once on startup
    rules_by_device = load_all_rules()
    rule_engine = RuleEngine(rules_by_device)

    print("✅ CoreLogic initialized. Waiting for unprocessed ticks...\n")

    while True:
        try:
            tick = db.get_next_unprocessed_state()
            if not tick:
                print("⏳ No unprocessed tick. Waiting...")
                time.sleep(TICK_INTERVAL)
                continue

            state_id, state_json = tick
            print(f"\n📦 Processing Tick ID: {state_id}")

            # Use MQTT-based live sensor values
            current_sensor_values = mqtt_listener.get_all_latest_values()
            db.insert_sensor_outputs(state_id, current_sensor_values)

            # Evaluate rules
            triggered_rules = rule_engine.evaluate_rules(current_sensor_values)
            if not triggered_rules:
                print("⚖️  No rules triggered.")

            for rule in triggered_rules:
                db.insert_rule_trigger(
                    state_id,
                    rule["rule_id"],
                    triggered=True,
                    conditions=rule["conditions"],
                    actions=rule["actions"]
                )
                for action in rule["actions"]:
                    device_manager.publish(
                        device_id=action["device_id"],
                        command=action["command"],
                        state_id=state_id
                    )

            db.mark_state_as_processed(state_id)
            print(f"✅ Tick {state_id} marked as processed.")
            time.sleep(TICK_INTERVAL)

        except Exception as e:
            import traceback
            print(f"\n❌ Error during tick processing: {e}")
            traceback.print_exc()
            time.sleep(TICK_INTERVAL)


if __name__ == "__main__":
    main()