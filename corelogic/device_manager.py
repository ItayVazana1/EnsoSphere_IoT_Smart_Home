"""
Module: corelogic/device_manager.py
Purpose: Manages all smart devices and handles command publishing logic.
Author: Itay Vazana
"""

from datetime import datetime
from corelogic.mqtt_client import MQTTClient
from devices.devices_registry import get_all_devices
from corelogic.db_connector import DBConnector



class DeviceManager:
    def __init__(self, mqtt_client: MQTTClient, db_connector: DBConnector):
        """
        Initializes the DeviceManager with all registered devices.

        Args:
            mqtt_client (MQTTClient): An instance of the MQTT client.
        """
        self.devices = get_all_devices()
        self.mqtt_client = mqtt_client
        self.db = db_connector

    def publish(self, device_id: str, command: dict, state_id: int, manual: bool = False):
        """
        Publishes a command to a device and logs the action to the database.

        Args:
            device_id (str): The device to command.
            command (dict): The command/state to apply.
            state_id (int): The current tick's state ID.
            manual (bool): Whether this command is manual (bypass checks).
        """
        device = self.devices.get(device_id)
        if not device:
            print(f"⚠️ Device '{device_id}' not found.")
            return

        if manual or device.should_update(command):
            print(f"📤 Publishing to {device_id}: {command} (manual={manual})")
            device.apply_state(self.mqtt_client, command, manual)

            self.db.insert_device_actions([
                {
                    "state_id": state_id,
                    "device_id": device_id,
                    "command": command,
                    "timestamp": datetime.utcnow().isoformat()
                }
            ])
        else:
            print(f"⏩ Skipped {device_id}: no change in state.")

    def get_all(self):
        """Returns the device dictionary."""
        return self.devices
