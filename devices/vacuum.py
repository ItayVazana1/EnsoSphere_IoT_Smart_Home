"""
Module: devices/vacuum.py
Purpose: Robot vacuum cleaner device for autonomous cleaning.
Author: Itay Vazana
"""

from devices.device import Device


class RobotVacuum(Device):
    def __init__(self, device_id: str):
        """
        Initialize a smart robot vacuum device.

        Args:
            device_id (str): Unique ID of the robot vacuum device.
        """
        super().__init__(device_id, topic=f"actuators/{device_id}")

    def should_update(self, new_state: dict) -> bool:
        """
        Compare 'status' (on/off) to determine if vacuum needs activation.

        Args:
            new_state (dict): Desired vacuum state.

        Returns:
            bool: True if state has changed.
        """
        if not self.last_state:
            return True
        return self.last_state.get("status") != new_state.get("status")

    def apply_state(self, mqtt_client, new_state: dict, manual: bool = False):
        """
        Apply new vacuum state with validation.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must include 'status'.
            manual (bool): Whether this is a manual override.
        """
        if "status" not in new_state:
            raise ValueError(f"RobotVacuum requires 'status' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, manual)
