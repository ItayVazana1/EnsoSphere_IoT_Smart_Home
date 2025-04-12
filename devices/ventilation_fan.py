"""
Module: devices/ventilation_fan.py
Purpose: Ventilation fan device for air circulation in bathrooms.
Author: Itay Vazana
"""

from devices.device import Device


class VentilationFan(Device):
    def __init__(self, device_id: str):
        """
        Initialize a smart ventilation fan device.

        Args:
            device_id (str): Unique ID of the ventilation fan.
        """
        super().__init__(device_id, topic=f"actuators/{device_id}")

    def should_update(self, new_state: dict) -> bool:
        """
        Compare 'status' field to detect fan state change.

        Args:
            new_state (dict): Desired command.

        Returns:
            bool: True if 'status' changed.
        """
        if not self.last_state:
            return True
        return self.last_state.get("status") != new_state.get("status")

    def apply_state(self, mqtt_client, new_state: dict, manual: bool = False):
        """
        Apply the new state to the ventilation fan with validation.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must contain 'status'.
            manual (bool): Whether this is a manual override.
        """
        if "status" not in new_state:
            raise ValueError(f"VentilationFan requires 'status' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, manual)
