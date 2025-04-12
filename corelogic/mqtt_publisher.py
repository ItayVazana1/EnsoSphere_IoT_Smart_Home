"""
Module: corelogic/mqtt_publisher.py
Purpose: Sends actions to devices via DeviceManager and MQTT.
Author: Itay Vazana
"""

from corelogic.device_manager import DeviceManager
from corelogic.mqtt_client import MQTTClient


class MQTTPublisher:
    def __init__(self):
        """
        Initializes the MQTT publisher and connects the MQTT client.
        """
        self.mqtt = MQTTClient()
        self.mqtt.connect()
        self.manager = DeviceManager(self.mqtt)

    def publish_actions(self, actions: list[dict]):
        """
        Publishes a list of triggered rule actions to devices.

        Args:
            actions (list): List of dicts containing:
                - device_id
                - command (dict)
                - (optional) manual (bool)
        """
        for action in actions:
            device_id = action["device_id"]
            command = action["command"]
            manual = action.get("manual", False)
            self.manager.publish(device_id, command, manual)

    def get_manager(self) -> DeviceManager:
        """
        Returns the internal device manager instance.
        """
        return self.manager
