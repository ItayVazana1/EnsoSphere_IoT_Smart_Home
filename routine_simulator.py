import os
import random
import time
import pandas as pd
from core.environment_manager import EnvironmentManager
from core.mqtt_client import create_mqtt_client
from core.rule_engine import process_all_rules

# --- Config ---
ROUTINE_DIR = "routines"
TIME_COLUMN = "Time"
SENSOR_COLUMN = "Triggered Sensors"


def choose_random_routine_file():
    files = [f for f in os.listdir(ROUTINE_DIR) if f.startswith("daily_routine_") and f.endswith(".xlsx")]
    if not files:
        raise FileNotFoundError("No routine files found in 'routines/' directory.")
    selected = random.choice(files)
    print(f"\n🎲 Selected routine file: {selected}\n")
    return os.path.join(ROUTINE_DIR, selected)


def simulate_routine():
    routine_path = choose_random_routine_file()
    df = pd.read_excel(routine_path)

    # Initialize environment and MQTT
    env_manager = EnvironmentManager()
    mqtt_client = create_mqtt_client()
    mqtt_client.loop_start()

    acceleration = env_manager.acceleration_factor
    print(f"🚀 Simulation time acceleration factor: 1 real sec = {acceleration} simulated minutes\n")

    for idx, row in df.iterrows():
        print(f"\n🕒 Time: {row[TIME_COLUMN]} | Event: {row['Event Description']}")

        # Parse triggered sensors (comma-separated string)
        sensor_data = {}
        triggered = str(row.get(SENSOR_COLUMN, "")).strip()
        if triggered:
            sensors = [s.strip() for s in triggered.split(",") if s.strip()]
            for sensor_id in sensors:
                sensor_data[sensor_id] = "detected"  # default simulated value

        # Get current environment data
        env_manager.update_time()
        env_data = env_manager.get_environment_data()

        # Process rules based on current data
        process_all_rules(
            rules=load_rules(),
            env_data=env_data,
            sensor_data=sensor_data,
            mqtt_client=mqtt_client
        )

        time.sleep(1)  # 1 sec real-time = X min simulated

    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("\n✅ Routine simulation completed.")


def load_rules():
    from core.rule_engine import load_json, RULES_PATH, SCHEMA_PATH, validate_rules
    rules_data = load_json(RULES_PATH)
    schema = load_json(SCHEMA_PATH)
    rules = rules_data.get("rules", [])

    if not validate_rules(rules, schema):
        raise ValueError("❌ Rules validation failed.")

    return rules


# --- Manual Run ---
if __name__ == "__main__":
    simulate_routine()
