"""
Module: corelogic/corelogic_main_static.py
Purpose: Passive silent mode – confirms ticks without triggering any device actions or logging.
Author: Itay Vazana
"""

import time
import os
import json
import mysql.connector
from dotenv import load_dotenv
import socket
from datetime import datetime

MAX_TICK_RETRIES = 5
TICK_RETRY_DELAY = 5  # seconds

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DB = os.getenv("MYSQL_DATABASE", "ensosphere")
MYSQL_USER = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")

def wait_for_mysql(host: str, port: int, timeout: int = 60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=5):
                return
        except (socket.timeout, ConnectionRefusedError):
            time.sleep(1)
    raise TimeoutError("MySQL not available after timeout.")

def get_next_unprocessed_state(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM state_raw WHERE processed_by_core = 0 ORDER BY id ASC LIMIT 1")
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None

def mark_state_as_processed(conn, state_id):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE state_raw SET processed_by_core = 1, processed_at = %s WHERE id = %s",
        (datetime.now(), state_id)
    )
    conn.commit()
    cursor.close()

def wait_for_first_tick(conn, max_wait=60):
    start = time.time()
    cursor = conn.cursor()
    while time.time() - start < max_wait:
        cursor.execute("SELECT COUNT(*) FROM state_raw")
        if cursor.fetchone()[0] > 0:
            return
        time.sleep(1)
    raise RuntimeError("No ticks found in DB after waiting.")

if __name__ == "__main__":
    wait_for_mysql(MYSQL_HOST, MYSQL_PORT)

    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        autocommit=True
    )

    wait_for_first_tick(conn)
    consecutive_empty_ticks = 0

    while True:
        try:
            cursor = conn.cursor()
            tick_id = get_next_unprocessed_state(conn)
            if tick_id:
                consecutive_empty_ticks = 0
                mark_state_as_processed(conn, tick_id)
            else:
                consecutive_empty_ticks += 1
                time.sleep(TICK_RETRY_DELAY)
                if consecutive_empty_ticks >= MAX_TICK_RETRIES:
                    break
        except:
            break
