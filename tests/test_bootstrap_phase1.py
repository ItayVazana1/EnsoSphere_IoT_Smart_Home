# Module: tests/test_bootstrap_phase1.py
# Purpose: Phase 1 verification - check MySQL + MQTT availability and response
# Run: python tests/test_bootstrap_phase1.py

import os
import time
import mysql.connector
import paho.mqtt.client as mqtt

# Load environment (optional if you run inside container)
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "ensosphere")
MYSQL_USER = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = 1883


def test_mysql_connection():
    print("🔍 Testing MySQL connection...")
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3307,
            user="root",
            password="root",
            database="ensosphere"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()
        print(f"✅ Connected to MySQL database: {result[0]}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")


def test_mqtt_connection():
    print("🔍 Testing MQTT broker connection...")

    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("✅ MQTT connection successful")
            client.disconnect()
        else:
            print(f"❌ MQTT connection failed: return code {rc}")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        time.sleep(2)  # Allow time for connection
        client.loop_stop()
    except Exception as e:
        print(f"❌ MQTT connection exception: {e}")


if __name__ == "__main__":
    print("🚀 Running Phase 1 Infrastructure Test")
    test_mysql_connection()
    test_mqtt_connection()
