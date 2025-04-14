"""
Module: corelogic/db_connector.py
Purpose: Handles database read/write operations for CoreLogic tick processing
Author: Itay Vazana
"""

import os
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Database connection configuration
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "ensosphere")
}


class DBConnector:
    def __init__(self):
        """
        Establishes a connection to the MySQL database.
        """
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

    def get_next_unprocessed_state(self):
        """
        Retrieves the next state_json that hasn't been processed yet by CoreLogic.

        Returns:
            tuple: (state_id: int, state_json: dict) or None if no unprocessed state exists.
        """
        query = """
            SELECT id, state_json FROM state_raw
            WHERE processed_by_core = 0
            ORDER BY id ASC LIMIT 1;
        """
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        if row:
            return row["id"], json.loads(row["state_json"])
        return None

    def insert_sensor_outputs(self, state_id, sensor_dict):
        """
        Inserts all sensor values into the sensor_outputs table for the given state_id.

        Args:
            state_id (int): The ID of the processed tick.
            sensor_dict (dict): Dictionary of sensor_id → value.
        """
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        query = """
            INSERT INTO sensor_outputs (state_id, sensor_id, value, evaluated_at)
            VALUES (%s, %s, %s, %s);
        """
        data = [(state_id, sensor_id, str(value), now) for sensor_id, value in sensor_dict.items()]
        self.cursor.executemany(query, data)
        self.conn.commit()

    def insert_rule_trigger(self, state_id, rule_id, triggered, conditions, actions):
        """
        Logs a rule evaluation result into the rule_triggers table.

        Args:
            state_id (int): Tick ID being processed.
            rule_id (str): ID of the evaluated rule.
            triggered (bool): Whether the rule was triggered.
            conditions (dict): The trigger condition block.
            actions (list): The list of device actions.
        """
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        query = """
            INSERT INTO rule_triggers
            (state_id, rule_id, triggered, conditions_json, actions_json, evaluated_at)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        values = (
            state_id,
            rule_id,
            int(triggered),
            json.dumps(conditions),
            json.dumps(actions),
            now
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def upsert_device_state(self, device_id, state_dict):
        """
        Inserts or updates the state of a device in the device_states table.

        Args:
            device_id (str): ID of the device.
            state_dict (dict): Device state (status, config, etc.)
        """
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        query = """
            INSERT INTO device_states (device_id, state_json, last_updated)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                state_json = VALUES(state_json),
                last_updated = VALUES(last_updated);
        """
        values = (device_id, json.dumps(state_dict), now)
        self.cursor.execute(query, values)
        self.conn.commit()

    def mark_state_as_processed(self, state_id):
        """
        Marks a tick as processed in the state_raw table.

        Args:
            state_id (int): The ID of the tick to mark.
        """
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        query = """
            UPDATE state_raw
            SET processed_by_core = 1, processed_at = %s
            WHERE id = %s;
        """
        self.cursor.execute(query, (now, state_id))
        self.conn.commit()

    def insert_device_action(self, state_id, device_id, command):
        """
        Logs a device command issued by CoreLogic into the device_actions table.

        Args:
            state_id (int): The tick ID.
            device_id (str): The target device.
            command (dict): The command sent to the device.
        """
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        query = """
            INSERT INTO device_actions (state_id, device_id, command_json, executed_at)
            VALUES (%s, %s, %s, %s);
        """
        values = (state_id, device_id, json.dumps(command), now)
        self.cursor.execute(query, values)
        self.conn.commit()

    def close(self):
        """
        Closes the database connection.
        """
        self.cursor.close()
        self.conn.close()