"""
Module: devices/security.py
Purpose: Smart security system device for home protection.
Author: Itay Vazana
"""

from devices.device import Device


class SecuritySystem(Device):
    def __init__(self, device_id: str):
        """
        Initialize a smart Security System device.

        Args:
            device_id (str): Unique ID of the security system device.
        """
        super().__init__(device_id, topic=f"actuators/{device_id}")

    def should_update(self, new_state: dict) -> bool:
        """
        Compares 'armed' field to detect security status change.

        Args:
            new_state (dict): Desired security system state.

        Returns:
            bool: True if state changed.
        """
        if not self.last_state:
            return True
        return self.last_state.get("armed") != new_state.get("armed")

    def apply_state(self, mqtt_client, new_state: dict, manual: bool = False):
        """
        Applies new armed/disarmed state to the system.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must contain 'armed': True/False.
            manual (bool): Whether this is a manual override.
        """
        # Normalize status → armed
        if "status" in new_state and "armed" not in new_state:
            if new_state["status"] == "armed":
                new_state["armed"] = True
            elif new_state["status"] == "disarmed":
                new_state["armed"] = False

        if "armed" not in new_state:
            raise ValueError(f"SecuritySystem requires 'armed' boolean in command: {new_state}")

        super().apply_state(mqtt_client, new_state, manual)

