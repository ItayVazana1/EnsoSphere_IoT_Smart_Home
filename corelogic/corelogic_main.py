import time
import json
from corelogic.db_connector import DBConnector
from corelogic.sensor_manager import SensorManager
from corelogic.rule_engine import RuleEngine

if __name__ == "__main__":
    print("🟡 EnsoSphere CoreLogic is alive. Starting processing loop...")
    db = DBConnector()
    sensors = SensorManager()
    engine = RuleEngine("corelogic/rules/")
    engine.load_rules_from_folder()

    while True:
        try:
            state = db.get_next_unprocessed_state()
            if state:
                print(f"\n✅ Processing state_id={state['state_id']}")

                # Parse JSON state
                state_json = json.loads(state["state_json"])

                # Evaluate sensors
                sensor_outputs = sensors.evaluate_sensors(state_json)

                print("📡 Sensor outputs:")
                for k, v in sensor_outputs.items():
                    print(f"   - {k}: {v}")

                # Write sensor outputs to DB
                db.insert_sensor_outputs(state["state_id"], sensor_outputs)

                # Evaluate rules and trigger actions
                triggered_actions = engine.evaluate_rules(state["state_id"], sensor_outputs)

                if triggered_actions:
                    print("🎯 Triggered rules:")
                    for action in triggered_actions:
                        print(f"   - {action['rule_id']} → {action['device_id']} → {action['command']}")

                    db.insert_rule_triggers(triggered_actions)
                    db.insert_device_states(triggered_actions)

                # Mark state as processed
                db.mark_state_as_processed(state["state_id"])
            else:
                print("⏸ No new states. Waiting...")
            time.sleep(5)
        except Exception as e:
            print("❌ Error during CoreLogic loop:")
            print(e)
            time.sleep(5)