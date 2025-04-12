"""
Module: corelogic/device_manager.py
Purpose: Manages all smart devices and handles command publishing logic.
Author: Itay Vazana
"""

from corelogic.mqtt_client import MQTTClient
from devices.devices_registry import get_all_devices


class DeviceManager:
    def __init__(self, mqtt_client: MQTTClient):
        """
        Initializes the DeviceManager with all registered devices.

        Args:
            mqtt_client (MQTTClient): An instance of the MQTT client.
        """
        self.devices = get_all_devices()
        self.mqtt_client = mqtt_client

    def publish(self, device_id: str, command: dict, manual: bool = False):
        """
        Publishes a command to a device if it needs to be updated.

        Args:
            device_id (str): The device to command.
            command (dict): The command/state to apply.
            manual (bool): Whether this command is manual (bypass checks).
        """
        device = self.devices.get(device_id)
        if not device:
            print(f"⚠️ Device '{device_id}' not found.")
            return

        if manual or device.should_update(command):
            print(f"📤 Publishing to {device_id}: {command} (manual={manual})")
            device.apply_state(self.mqtt_client, command, manual)
        else:
            print(f"⏩ Skipped {device_id}: no change in state.")

    def get_all(self):
        """Returns the device dictionary."""
        return self.devices
