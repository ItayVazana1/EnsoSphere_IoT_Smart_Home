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

# Load MQTT configuration from .env
load_dotenv()
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", 60))
LOG_FILE = os.path.join(os.path.dirname(__file__), "mqtt_log.txt")


def log_to_file(topic: str, payload: dict):
    """
    Appends a sensor MQTT message to the local log file with a UTC timestamp.

    Args:
        topic (str): MQTT topic the message came from.
        payload (dict): Decoded JSON payload from the message.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {topic} → {json.dumps(payload)}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

    print(log_entry.strip())


def on_connect(client, userdata, flags, rc):
    """
    Callback for MQTT connection result. Subscribes to sensor topics on success.
    """
    if rc == 0:
        print("✅ Connected to MQTT broker. Subscribed to sensor/#")
        client.subscribe("sensor/#")
    else:
        print(f"❌ MQTT connection failed (code {rc})")


def on_message(client, userdata, msg):
    """
    Callback for incoming MQTT messages.
    Attempts to parse and log JSON payloads.
    """
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        log_to_file(msg.topic, payload)
    except Exception as e:
        print(f"⚠️ Failed to decode MQTT message on topic {msg.topic}: {e}")


def start_sniffer():
    """
    Starts the MQTT sniffer client to listen and log sensor messages.
    """
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
    client.loop_forever()


if __name__ == "__main__":
    start_sniffer()
