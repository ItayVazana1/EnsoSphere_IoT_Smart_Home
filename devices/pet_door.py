"""
Module: devices/pet_door.py
Purpose: Smart pet door device for pet entry and exit.
Author: Itay Vazana
"""

from devices.device import Device


class PetDoor(Device):
    def __init__(self, device_id: str):
        """
        Initialize a smart Pet Door device.

        Args:
            device_id (str): Unique ID of the Pet Door device.
        """
        super().__init__(device_id, topic=f"actuators/{device_id}")

    def should_update(self, new_state: dict) -> bool:
        """
        Compares 'status' field for determining door change.

        Args:
            new_state (dict): Desired command for pet door.

        Returns:
            bool: True if door state changed.
        """
        if not self.last_state:
            return True
        return self.last_state.get("status") != new_state.get("status")

    def apply_state(self, mqtt_client, new_state: dict, manual: bool = False):
        """
        Applies new pet door state with validation.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must contain 'status'.
            manual (bool): Whether this is a manual override.
        """
        if "status" not in new_state:
            raise ValueError(f"PetDoor device requires 'status' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, manual)
