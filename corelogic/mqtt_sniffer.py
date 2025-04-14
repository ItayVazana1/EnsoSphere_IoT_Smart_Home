"""
Module: corelogic/mqtt_sniffer.py
Purpose: Passive MQTT listener that logs all sensor messages to a local text file.
Author: Itay Vazana
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# Load MQTT configuration
load_dotenv()
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", 60))
LOG_FILE = "corelogic/mqtt_log.txt"


def log_to_file(topic: str, payload: dict):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {topic} → {json.dumps(payload)}\n"
        f.write(log_entry)
        print(log_entry.strip())


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT broker. Listening to sensor topics...")
        client.subscribe("sensor/#")
    else:
        print(f"❌ MQTT connection failed with code {rc}")


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        log_to_file(msg.topic, payload)
    except Exception as e:
        print(f"⚠️ Failed to decode MQTT message: {e}")


def start_sniffer():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
    client.loop_forever()


if __name__ == "__main__":
    start_sniffer()