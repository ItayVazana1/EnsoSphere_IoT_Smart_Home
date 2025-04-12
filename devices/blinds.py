"""
Module: devices/blinds.py
Purpose: Smart blinds device supporting open/close states.
Author: Itay Vazana
"""

from devices.device import Device


class Blinds(Device):
    def __init__(self, device_id: str):
        """
        Initialize a smart Blinds device.

        Args:
            device_id (str): Unique ID of the Blinds device.
        """
        super().__init__(device_id, topic=f"actuators/{device_id}")

    def should_update(self, new_state: dict) -> bool:
        """
        Compare 'position' field to determine if update is required.

        Args:
            new_state (dict): New desired state for the blinds.

        Returns:
            bool: True if position changed, False otherwise.
        """
        if not self.last_state:
            return True
        return self.last_state.get("position") != new_state.get("position")

    def apply_state(self, mqtt_client, new_state: dict, manual: bool = False):
        """
        Apply the new position state to the smart blinds.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must contain 'position' key.
            manual (bool): Whether this is a manual override.
        """
        if "position" not in new_state:
            raise ValueError(f"Blinds device requires 'position' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, manual)
