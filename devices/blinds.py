"""
Module: devices/blinds.py
Purpose: Smart blinds device supporting open/close states.
Author: Itay Vazana
"""

from devices.device import Device


class Blinds(Device):
    def __init__(self, device_id: str, metadata: dict):
        """
        Initialize a smart Blinds device.

        Args:
            device_id (str): Unique ID of the Blinds device.
            metadata (dict): Metadata for this device type from device_metadata.json
        """
        super().__init__(device_id, topic=f"actuators/{device_id}", metadata=metadata)

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

    def apply_state(self, mqtt_client, new_state: dict, state_id: int = None, manual: bool = False):
        """
        Apply the new state to the Blinds device.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): New desired state (open/close or position).
            state_id (int): Tick ID for traceability.
            manual (bool): Whether this is a manual override.
        """
        # Normalize status → position
        if "position" not in new_state:
            if new_state.get("status") == "open":
                new_state["position"] = "up"
            elif new_state.get("status") == "closed":
                new_state["position"] = "down"

        if "position" not in new_state:
            raise ValueError(f"Blinds device requires 'position' or valid status: {new_state}")

        super().apply_state(mqtt_client, new_state, state_id=state_id, manual=manual)
