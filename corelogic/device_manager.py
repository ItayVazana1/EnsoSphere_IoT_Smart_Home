"""
Module: corelogic/device_manager.py
Purpose: Manages all smart devices and handles command publishing logic.
Author: Itay Vazana
"""

from datetime import datetime
from devices.devices_registry import get_all_devices
from corelogic.db_connector import DBConnector
from corelogic.mqtt_publisher import MQTTPublisher


class DeviceManager:
    def __init__(self, mqtt_publisher: MQTTPublisher, db_connector: DBConnector):
        """
        Initializes the DeviceManager with all registered devices.

        Args:
            mqtt_publisher (MQTTPublisher): Handles publishing commands to MQTT.
            db_connector (DBConnector): Handles DB operations for devices.
        """
        self.devices = get_all_devices()
        self.mqtt_publisher = mqtt_publisher
        self.db = db_connector

    def publish(self, device_id: str, command: dict, state_id: int, manual: bool = False):
        """
        Publishes a command to a device and logs it to the database.

        Args:
            device_id (str): Target device ID.
            command (dict): Command to apply.
            state_id (int): Current tick ID.
            manual (bool): Force execution even if state hasn't changed.
        """
        device = self.devices.get(device_id)
        if not device:
            print(f"[DeviceManager] ⚠️ Device '{device_id}' not found.")
            return

        if manual or device.should_update(command):
            print(f"[DeviceManager] 📤 Executing command for {device_id}: {command} (manual={manual})")
            device.apply_state(self.mqtt_publisher.client, command, manual)

            # Log to DB
            self.db.upsert_device_state(device_id, command)
            self.db.insert_device_action(state_id, device_id, command)
        else:
            print(f"[DeviceManager] ⏩ No state change for {device_id}, skipping.")

    def get_all(self):
        """Returns the dictionary of all devices."""
        return self.devices
