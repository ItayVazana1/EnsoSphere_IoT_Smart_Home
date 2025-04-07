"""
Test DBConnector – Direct MySQL Access
Run this outside Docker to test DB connectivity and functionality
"""

import json
from datetime import datetime
import mysql.connector


class DBConnector:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'port': 3307,
            'user': 'user',
            'password': 'password',
            'database': 'ensosphere',
            'autocommit': True
        }

    def _connect(self):
        return mysql.connector.connect(**self.config)

    def get_next_unprocessed_state(self):
        query = """
            SELECT id, state_json FROM state_raw
            WHERE processed_by_core = 0
            ORDER BY id ASC LIMIT 1
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            return {"state_id": row[0], "state_json": row[1]} if row else None

    def mark_state_as_processed(self, state_id):
        query = """
            UPDATE state_raw
            SET processed_by_core = 1, processed_at = %s
            WHERE id = %s
        """
        timestamp = datetime.utcnow().isoformat()
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (timestamp, state_id))

    def insert_sensor_outputs(self, state_id, sensor_outputs):
        query = """
            INSERT INTO sensor_outputs (state_id, sensor_id, value, evaluated_at)
            VALUES (%s, %s, %s, %s)
        """
        timestamp = datetime.utcnow().isoformat()
        with self._connect() as conn:
            cursor = conn.cursor()
            for sensor_id, value in sensor_outputs.items():
                cursor.execute(query, (state_id, sensor_id, str(value), timestamp))

    def insert_rule_triggers(self, state_id, rule_results):
        query = """
            INSERT INTO rule_triggers (state_id, rule_id, triggered, conditions_json, actions_json, evaluated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        timestamp = datetime.utcnow().isoformat()
        with self._connect() as conn:
            cursor = conn.cursor()
            for result in rule_results:
                cursor.execute(query, (
                    state_id,
                    result['rule_id'],
                    int(result['triggered']),
                    result['conditions_json'],
                    result['actions_json'],
                    timestamp
                ))

    def upsert_device_state(self, device_id, state_json, timestamp=None):
        if not timestamp:
            timestamp = datetime.utcnow().isoformat()
        query = """
            INSERT INTO device_states (device_id, state_json, last_updated)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
              state_json = VALUES(state_json),
              last_updated = VALUES(last_updated)
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (device_id, state_json, timestamp))


# --- Run the test
if __name__ == "__main__":
    db = DBConnector()

    print("🔍 Fetching next unprocessed state...")
    state = db.get_next_unprocessed_state()
    if not state:
        print("❌ No unprocessed state found.")
        exit(1)

    state_id = state['state_id']
    print(f"✅ Got state_id={state_id}")

    print("📝 Inserting test sensor_outputs...")
    db.insert_sensor_outputs(state_id, {
        "motion_kitchen": True,
        "temperature_livingroom": 25.5
    })

    print("🧠 Inserting test rule_triggers...")
    db.insert_rule_triggers(state_id, [
        {
            "rule_id": "test_rule_lights_kitchen",
            "triggered": True,
            "conditions_json": json.dumps([
                {"sensor": "motion_kitchen", "equals": True}
            ]),
            "actions_json": json.dumps([
                {"device": "lights_kitchen", "command": {"status": "on"}}
            ])
        }
    ])

    print("💡 Upserting test device state...")
    db.upsert_device_state("lights_kitchen", json.dumps({"status": "on"}))

    print("✅ Marking state as processed...")
    db.mark_state_as_processed(state_id)

    print("🎉 Done! DBConnector test completed.")
