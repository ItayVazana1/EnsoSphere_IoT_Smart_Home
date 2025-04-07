"""
Module: corelogic/db_connector.py
Purpose: Handle all database interactions for CoreLogic engine (MySQL version)
Author: Itay Vazana
"""

import os
import mysql.connector
from datetime import datetime
from typing import Optional, Dict, Any, List


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
        """
        Retrieves the next unprocessed state from state_raw.

        Returns:
            dict or None: Row containing id, state_json if available.
        """
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
        """
        Marks a state as processed in state_raw.

        Args:
            state_id (int): ID of the state to mark.
        """
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
        """
        Inserts sensor output values into sensor_outputs table.

        Args:
            state_id (int): Associated state ID.
            sensor_outputs (dict): Dictionary of {sensor_id: value}
        """
        query = """
            INSERT INTO sensor_outputs (state_id, sensor_id, value, evaluated_at)
            VALUES (%s, %s, %s, %s)
        """
        timestamp = datetime.utcnow().isoformat()
        with self._connect() as conn:
            cursor = conn.cursor()
            for sensor_id, value in sensor_outputs.items():
                cursor.execute(query, (state_id, sensor_id, str(value), timestamp))

    def insert_rule_triggers(self, state_id: int, rule_results: List[Dict[str, Any]]):
        """
        Inserts rule evaluation results into rule_triggers table.

        Args:
            state_id (int): Tick ID.
            rule_results (list): List of rule trigger data dicts with keys:
                - rule_id, triggered (bool), conditions_json (str), actions_json (str)
        """
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

    def upsert_device_state(self, device_id: str, state_json: str, timestamp: Optional[str] = None):
        """
        Inserts or updates device state in device_states table.

        Args:
            device_id (str): Unique ID of device.
            state_json (str): JSON string of current state.
            timestamp (str): Optional UTC timestamp. Defaults to now.
        """
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