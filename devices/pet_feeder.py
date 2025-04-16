"""
Module: devices/pet_feeder.py
Purpose: Smart pet feeder device to dispense food on schedule.
Author: Itay Vazana
"""

from devices.device import Device


class PetFeeder(Device):
    def __init__(self, device_id: str, metadata: dict):
        """
        Initialize a smart Pet Feeder device.

        Args:
            device_id (str): Unique ID of the pet feeder device.
            metadata (dict): Metadata for this device type from device_metadata.json
        """
        super().__init__(device_id, topic=f"actuators/{device_id}", metadata=metadata)

    def should_update(self, new_state: dict) -> bool:
        """
        Compares the 'dispense' flag to determine if feeding is requested.

        Args:
            new_state (dict): Desired action for the feeder.

        Returns:
            bool: True if 'dispense' is True.
        """
        return new_state.get("dispense", False) is True

    def apply_state(self, mqtt_client, new_state: dict, state_id: int = None, manual: bool = False):
        """
        Triggers the pet feeder to dispense food.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must contain 'dispense': True.
            state_id (int): Tick ID for traceability.
            manual (bool): Whether this is a manual override.
        """
        if new_state.get("action") == "dispense":
            new_state["dispense"] = True

        if new_state.get("dispense") is not True:
            raise ValueError(f"PetFeeder requires 'dispense': True in command: {new_state}")

        super().apply_state(mqtt_client, new_state, state_id=state_id, manual=manual)
        self.last_state = None  # Allow repeated dispensing
