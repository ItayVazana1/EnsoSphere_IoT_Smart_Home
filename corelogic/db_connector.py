"""
Module: corelogic/db_connector.py
Purpose: Handle all database interactions for CoreLogic engine (MySQL version)
Author: Itay Vazana
"""
import json
import os
import mysql.connector
from datetime import datetime
from typing import Optional, Dict, Any, List
from json import dumps  # Used for ensuring JSON compatibility

class DBConnector:
    def __init__(self):
        """
        Initialize the MySQL database connector using environment variables.
        """
        self.config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': os.getenv('MYSQL_DATABASE', 'ensosphere'),
            'autocommit': True
        }

    def _connect(self):
        return mysql.connector.connect(**self.config)

    def get_next_unprocessed_state(self) -> Optional[Dict[str, Any]]:
        query = """
            SELECT id, state_json FROM state_raw
            WHERE processed_by_core = 0
            ORDER BY id ASC LIMIT 1
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                return {"state_id": row[0], "state_json": row[1]}
            return None

    def mark_state_as_processed(self, state_id: int):
        query = """
            UPDATE state_raw
            SET processed_by_core = 1, processed_at = %s
            WHERE id = %s
        """
        timestamp = datetime.utcnow().isoformat()
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (timestamp, state_id))

    def insert_sensor_outputs(self, state_id: int, sensor_outputs: Dict[str, Any]):
        query = """
            INSERT INTO sensor_outputs (state_id, sensor_id, value, evaluated_at)
            VALUES (%s, %s, %s, %s)
        """
        timestamp = datetime.utcnow().isoformat()
        with self._connect() as conn:
            cursor = conn.cursor()
            for sensor_id, value in sensor_outputs.items():
                cursor.execute(query, (state_id, sensor_id, str(value), timestamp))

    def insert_rule_triggers(self, rule_results: List[Dict[str, Any]]):
        query = """
            INSERT INTO rule_triggers (state_id, rule_id, triggered, conditions_json, actions_json, evaluated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            for result in rule_results:
                cursor.execute(query, (
                    result['state_id'],
                    result['rule_id'],
                    int(result.get('triggered', 1)),
                    dumps(result.get('conditions_json', {})),
                    dumps(result.get('actions_json', {})),
                    result['timestamp']
                ))

    def insert_device_states(self, device_states: List[Dict[str, Any]]):
        query = """
            INSERT INTO device_states (device_id, state_json, last_updated)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                state_json = VALUES(state_json),
                last_updated = VALUES(last_updated)
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            for state in device_states:
                try:
                    if isinstance(state, str):
                        state = json.loads(state)

                    if not isinstance(state, dict):
                        continue

                    device_id = state.get('device_id')
                    command = state.get('command')
                    timestamp = state.get('timestamp')

                    if isinstance(command, str):
                        try:
                            command = json.loads(command)
                        except json.JSONDecodeError:
                            continue

                    cursor.execute(query, (
                        device_id,
                        dumps(command),
                        timestamp
                    ))
                except Exception:
                    continue

    def upsert_device_state(self, device_id: str, state_json: str, timestamp: Optional[str] = None):
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

    def get_device_current_state(self, device_id: str) -> Optional[Dict[str, Any]]:
        query = """
            SELECT state_json FROM device_states
            WHERE device_id = %s
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (device_id,))
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return None

    def insert_device_actions(self, device_actions: List[Dict[str, Any]]):
        """
        Insert device action records for a specific tick.

        Args:
            device_actions: A list of dicts with keys: state_id, device_id, command, timestamp (optional).
        """
        query = """
            INSERT INTO device_actions (state_id, device_id, command_json, executed_at)
            VALUES (%s, %s, %s, %s)
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            for action in device_actions:
                try:
                    state_id = action["state_id"]
                    device_id = action["device_id"]
                    command = action["command"]
                    executed_at = action.get("timestamp", datetime.utcnow().isoformat())

                    cursor.execute(query, (
                        state_id,
                        device_id,
                        dumps(command),
                        executed_at
                    ))
                except Exception:
                    continue
