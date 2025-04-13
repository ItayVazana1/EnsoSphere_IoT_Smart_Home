"""
Module: simulator/sensor_publisher.py
Purpose: Publishes sensor outputs from simulator to MQTT broker.
Author: Itay Vazana
"""

import os
from simulator.mqtt_client import MQTTClient

# Optional concise output mode
CONCISE_MODE = os.getenv("MQTT_PUBLISHER_CONCISE_MODE", "False").lower() in ("1", "true", "yes")


class SensorPublisher:
    def __init__(self):
        self.mqtt = MQTTClient()
        self.mqtt.connect()

    def publish_sensor_outputs(self, sensor_outputs: dict):
        """
        Publishes each sensor output to its respective MQTT topic.

        Args:
            sensor_outputs (dict): Mapping of sensor_id → value
        """
        for sensor_id, value in sensor_outputs.items():
            topic = f"sensor/{sensor_id}"
            payload = {"value": value}
            self.mqtt.publish(topic, payload)

            if not CONCISE_MODE:
                print(f"📤 Published {sensor_id} → {value}")
