"""
Module: simulator/mqtt_client.py
Purpose: MQTT client for publishing sensor values from simulator.
Author: Itay Vazana
"""

import paho.mqtt.client as mqtt
import os
import json
from dotenv import load_dotenv

load_dotenv()

MQTT_HOST = os.getenv("MQTT_BROKER", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", 60))


class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.connected = False

    def connect(self):
        try:
            self.client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
            self.client.loop_start()
            self.connected = True
            print(f"📡 Connected to MQTT broker at {MQTT_HOST}:{MQTT_PORT}")
        except Exception as e:
            print(f"❌ Failed to connect to MQTT broker: {e}")
            self.connected = False

    def publish(self, topic: str, payload: dict):
        if self.connected:
            self.client.publish(topic, json.dumps(payload))
        else:
            print(f"⚠️ MQTT not connected. Could not publish to topic '{topic}'")
