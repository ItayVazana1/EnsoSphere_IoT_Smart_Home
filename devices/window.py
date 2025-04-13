"""
Module: devices/window.py
Purpose: Smart window device for automated open/close control.
Author: Itay Vazana
"""

from devices.device import Device


class SmartWindow(Device):
    def __init__(self, device_id: str):
        """
        Initialize a smart Window device.

        Args:
            device_id (str): Unique ID of the smart window device.
        """
        super().__init__(device_id, topic=f"actuators/{device_id}")

    def should_update(self, new_state: dict) -> bool:
        """
        Compares 'position' field to detect change (e.g., 'open' or 'closed').

        Args:
            new_state (dict): Desired state.

        Returns:
            bool: True if position changed.
        """
        if not self.last_state:
            return True
        return self.last_state.get("position") != new_state.get("position")

    def apply_state(self, mqtt_client, new_state: dict, manual: bool = False):
        """
        Applies new position state to the window.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must include 'position'.
            manual (bool): Whether this is a manual override.
        """
        # Normalize 'status' → 'position'
        if "status" in new_state and "position" not in new_state:
            new_state["position"] = new_state["status"]

        if "position" not in new_state:
            raise ValueError(f"SmartWindow requires 'position' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, manual)
