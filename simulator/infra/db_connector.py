"""
Module: simulator/db_connector.py
Purpose: Manages all database interactions for the simulator, including state_json insertion.
Author: Itay Vazana
"""

import mysql.connector
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "ensosphere")
}


class DBConnector:
    def __init__(self):
        self.conn = None

    def wait_for_db(self, retries=10, delay=2):
        for attempt in range(retries):
            try:
                print(f"⏳ Attempting DB connection... ({attempt+1}/{retries})")
                self.conn = mysql.connector.connect(**DB_CONFIG)
                self.conn.close()
                print("✅ Database is up!")
                return
            except mysql.connector.Error:
                print("❌ DB not ready, retrying...")
                time.sleep(delay)
        raise RuntimeError("🛑 Could not connect to DB after multiple retries.")

    def connect(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)

    def close(self):
        if self.conn:
            self.conn.close()

    def insert_state(self, state: dict):
        cursor = self.conn.cursor()
        insert_query = """
        INSERT INTO state_raw (
            timestamp,
            simulation_time,
            season,
            is_daytime,
            temperature,
            weather,
            state_json,
            processed_by_core
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            state["timestamp"],
            state["simulation_time"],
            state["season"],
            state["is_daytime"],
            state["temperature"],
            state["weather"],
            json.dumps(state),
            False
        ))
        self.conn.commit()
        cursor.close()
