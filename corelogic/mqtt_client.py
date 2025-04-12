"""
Module: corelogic/mqtt_client.py
Purpose: Wrapper for MQTT connectivity and publishing.
Author: Itay Vazana
"""

import os
import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self):
        """
        Initializes the MQTT client using environment variables.
        """
        self.broker = os.getenv("MQTT_BROKER", "localhost")
        self.port = int(os.getenv("MQTT_PORT", 1883))
        self.client = mqtt.Client()

    def connect(self):
        """
        Connects to the MQTT broker.
        """
        try:
            self.client.connect(self.broker, self.port)
            self.client.loop_start()
            print(f"✅ Connected to MQTT broker at {self.broker}:{self.port}")
        except Exception as e:
            print(f"❌ MQTT connection failed: {e}")

    def publish(self, topic: str, payload: str):
        """
        Publishes a message to a topic.

        Args:
            topic (str): MQTT topic.
            payload (str): Message to send.
        """
        result = self.client.publish(topic, payload)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"📡 Published to {topic}: {payload}")
        else:
            print(f"⚠️ Failed to publish to {topic}: {result.rc}")
