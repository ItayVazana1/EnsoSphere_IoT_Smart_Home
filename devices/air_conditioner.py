"""
Module: devices/air_conditioner.py
Purpose: Air Conditioner device with support for on/off and temperature settings.
Author: Itay Vazana
"""

from devices.device import Device


class AirConditioner(Device):
    def __init__(self, device_id: str):
        """
        Initialize a smart Air Conditioner device.

        Args:
            device_id (str): Unique ID of the AC device.
        """
        super().__init__(device_id, topic=f"actuators/{device_id}")

    def should_update(self, new_state: dict) -> bool:
        """
        Compares 'status' and 'temperature' for determining state change.

        Args:
            new_state (dict): New desired state.

        Returns:
            bool: True if update needed, False otherwise.
        """
        if not self.last_state:
            return True
        return any([
            self.last_state.get("status") != new_state.get("status"),
            self.last_state.get("temperature") != new_state.get("temperature")
        ])

    def apply_state(self, mqtt_client, new_state: dict, manual: bool = False):
        """
        Apply new AC state with required field validation.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): State dict with at least 'status'.
            manual (bool): Whether this is a manual override.
        """
        # Normalize shorthand status → detailed
        if "status" in new_state:
            if new_state["status"] == "off":
                new_state.setdefault("mode", "off")
            elif new_state["status"] == "on":
                new_state.setdefault("mode", "cool")

        if "status" not in new_state:
            raise ValueError(f"AirConditioner requires 'status' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, manual)