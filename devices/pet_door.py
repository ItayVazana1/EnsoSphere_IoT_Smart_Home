"""
Module: devices/pet_door.py
Purpose: Smart pet door for Luna the dog.
Author: Itay Vazana
"""

from devices.device import Device


class PetDoor(Device):
    def __init__(self, device_id: str):
        """
        Initialize a smart Pet Door device.

        Args:
            device_id (str): Unique ID of the pet door.
        """
        super().__init__(device_id, topic=f"actuators/{device_id}")

    def should_update(self, new_state: dict) -> bool:
        """
        Compares 'status' field to determine if door state has changed.

        Args:
            new_state (dict): New desired state for the pet door.

        Returns:
            bool: True if status changed, otherwise False.
        """
        if not self.last_state:
            return True
        return self.last_state.get("status") != new_state.get("status")

    def apply_state(self, mqtt_client, new_state: dict, manual: bool = False):
        """
        Apply the new state to the pet door with validation.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must contain 'status' key.
            manual (bool): Whether this is a manual override.
        """
        # Normalize shorthand
        if "mode" in new_state and "status" not in new_state:
            new_state["status"] = new_state["mode"]

        if "status" not in new_state:
            raise ValueError(f"PetDoor requires 'status' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, manual)
