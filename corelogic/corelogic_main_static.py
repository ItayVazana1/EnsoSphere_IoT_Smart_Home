"""
Module: corelogic/corelogic_main_static.py
Purpose: Passive mode – confirms simulator ticks and listens to MQTT sensor messages.
Author: Itay Vazana
"""

import time
import os
import json
import mysql.connector
from dotenv import load_dotenv
import socket
from datetime import datetime
import paho.mqtt.client as mqtt

# --- Load configuration ---
load_dotenv()

# DB Config
MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DB = os.getenv("MYSQL_DATABASE", "ensosphere")
MYSQL_USER = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")

# MQTT Config
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", 60))

# Static mode configuration
LOG_FILE = os.path.join(os.path.dirname(__file__), "mqtt_log.txt")
MAX_TICK_RETRIES = 5
TICK_RETRY_DELAY = 5  # seconds


# --- MySQL helper functions ---
def wait_for_mysql(host: str, port: int, timeout: int = 60):
    print(f"⏳ Waiting for MySQL at {host}:{port}...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=5):
                print("✅ MySQL is available.")
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
        (datetime.utcnow(), state_id)
    )
    conn.commit()
    cursor.close()


def wait_for_first_tick(conn, max_wait=60):
    print("⏳ Waiting for first tick from simulator...")
    start = time.time()
    cursor = conn.cursor()
    while time.time() - start < max_wait:
        cursor.execute("SELECT COUNT(*) FROM state_raw")
        if cursor.fetchone()[0] > 0:
            print("✅ Tick data found. Beginning passive monitoring.")
            return
        time.sleep(1)
    raise RuntimeError("⛔ No ticks found in DB after waiting.")


# --- MQTT sniffer ---
def log_to_file(topic: str, payload: dict):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {topic} → {json.dumps(payload)}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(log_entry.strip())


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT connected. Subscribed to sensor/#")
        client.subscribe("sensor/#")
    else:
        print(f"❌ MQTT connection failed with code {rc}")


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        log_to_file(msg.topic, payload)
    except Exception as e:
        print(f"⚠️ Failed to decode MQTT message: {e}")


def start_mqtt_sniffer():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
    client.loop_start()


# --- Main passive logic ---
if __name__ == "__main__":
    print("\n📡 CoreLogic STATIC MODE – Listening to MQTT and confirming tick flow.\n")

    wait_for_mysql(MYSQL_HOST, MQTT_PORT)
    start_mqtt_sniffer()

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
            tick_id = get_next_unprocessed_state(conn)
            if tick_id:
                consecutive_empty_ticks = 0
                mark_state_as_processed(conn, tick_id)
                print(f"📝 Tick {tick_id} marked as processed.")
            else:
                consecutive_empty_ticks += 1
                print(f"⏳ Waiting for tick... [{consecutive_empty_ticks}/{MAX_TICK_RETRIES}]")
                time.sleep(TICK_RETRY_DELAY)
                if consecutive_empty_ticks >= MAX_TICK_RETRIES:
                    print("🛑 Too many empty attempts. Exiting static mode.")
                    break
        except Exception as e:
            print(f"❌ Error during static mode loop: {e}")
            break