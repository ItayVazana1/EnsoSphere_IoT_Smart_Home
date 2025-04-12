"""
Module: devices/door_lock.py
Purpose: Smart door lock device that manages lock/unlock states.
Author: Itay Vazana
"""

from devices.device import Device


class DoorLock(Device):
    def __init__(self, device_id: str):
        """
        Initialize a smart Door Lock device.

        Args:
            device_id (str): Unique ID of the Door Lock device.
        """
        super().__init__(device_id, topic=f"actuators/{device_id}")

    def should_update(self, new_state: dict) -> bool:
        """
        Compare 'locked' field to determine if update is required.

        Args:
            new_state (dict): New desired state for the door lock.

        Returns:
            bool: True if lock state changed, False otherwise.
        """
        if not self.last_state:
            return True
        return self.last_state.get("locked") != new_state.get("locked")

    def apply_state(self, mqtt_client, new_state: dict, manual: bool = False):
        """
        Apply the new lock state to the smart door lock.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must contain 'locked' key (True/False).
            manual (bool): Whether this is a manual override.
        """
        if "locked" not in new_state:
            raise ValueError(f"DoorLock requires 'locked' boolean in command: {new_state}")

        super().apply_state(mqtt_client, new_state, manual)
