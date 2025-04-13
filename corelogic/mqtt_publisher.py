"""
Module: corelogic/mqtt_publisher.py
Purpose: Optional utility for direct MQTT message publishing (no DB interaction)
Author: Itay Vazana
"""

from corelogic.mqtt_client import MQTTClient
import json
from datetime import datetime


class MQTTPublisher:
    def __init__(self):
        """
        Initializes the MQTT publisher with a direct client.
        """
        self.mqtt = MQTTClient()
        self.mqtt.connect()

    def publish(self, device_id: str, command: dict):
        """
        Publishes a single command to the MQTT topic of a device.

        Args:
            device_id (str): The device to publish to.
            command (dict): The command/state to send.
        """
        topic = f"ensosphere/devices/{device_id}"
        payload = json.dumps({
            "device_id": device_id,
            "command": command,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.mqtt.publish(topic, payload)

    def publish_batch(self, actions: list[dict]):
        """
        Publishes multiple device commands (no DB logging).

        Args:
            actions (list): List of dicts with device_id and command.
        """
        for action in actions:
            self.publish(
                device_id=action["device_id"],
                command=action["command"]
            )
