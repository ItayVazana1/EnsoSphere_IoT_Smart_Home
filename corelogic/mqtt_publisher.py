"""
Module: corelogic/mqtt_publisher.py
Purpose: Publishes MQTT commands to devices
Author: Itay Vazana
"""

import os
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", 60))


class MQTTPublisher:
    def __init__(self):
        """
        Initializes and connects the MQTT client for publishing.
        """
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        self.client.loop_start()
        print(f"[MQTT Publisher] Connected to broker at {MQTT_BROKER}:{MQTT_PORT}")

    def publish(self, device_id: str, command: dict, state_id: int):
        """
        Publishes a command to the corresponding device topic.

        Args:
            device_id (str): Target device identifier.
            command (dict): Command to send to the device.
            state_id (int): The tick ID to associate with this command.
        """
        topic = f"device/{device_id}"
        payload = {
            "device_id": device_id,
            "command": command,
            "state_id": state_id
        }

        try:
            self.client.publish(topic, json.dumps(payload))
            print(f"[MQTT Publisher] 📤 Published to {topic}: {payload}")
        except Exception as e:
            print(f"[MQTT Publisher] ❌ Failed to publish to {topic}: {e}")
