"""
Module: devices/window.py
Purpose: Smart window device for automated open/close control.
Author: Itay Vazana
"""

from devices.device import Device


class SmartWindow(Device):
    def __init__(self, device_id: str, metadata: dict):
        """
        Initialize a smart Window device.

        Args:
            device_id (str): Unique ID of the smart window device.
            metadata (dict): Metadata for this device type from device_metadata.json
        """
        super().__init__(device_id, topic=f"actuators/{device_id}", metadata=metadata)

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

    def apply_state(self, mqtt_client, new_state: dict, state_id: int = None, manual: bool = False):
        """
        Applies new position state to the window.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must include 'position'.
            state_id (int): Tick ID for traceability.
            manual (bool): Whether this is a manual override.
        """
        if "status" in new_state and "position" not in new_state:
            new_state["position"] = new_state["status"]

        if "position" not in new_state:
            raise ValueError(f"SmartWindow requires 'position' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, state_id=state_id, manual=manual)

    def get_temperature_effect(self) -> float:
        """
        Returns the temperature change caused by window position.

        Returns:
            float: Temperature delta (e.g., -0.3 when open).
        """
        if not self.last_state:
            return 0.0
        position = self.last_state.get("position")
        effect = self.get_environment_effect(position)
        return effect.get("temperature", 0.0)
