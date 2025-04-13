"""
Module: devices/tv.py
Purpose: Smart TV device with specific behavior for on/off states.
Author: Itay Vazana
"""

from devices.device import Device


class TV(Device):
    def __init__(self, device_id: str):
        """
        Initialize a smart TV device.

        Args:
            device_id (str): Unique ID of the TV device.
        """
        super().__init__(device_id, topic=f"actuators/{device_id}")

    def should_update(self, new_state: dict) -> bool:
        """
        Overrides base logic to compare only the 'status' field for TV.

        Args:
            new_state (dict): New desired state for the TV.

        Returns:
            bool: True if status has changed, False otherwise.
        """
        if not self.last_state:
            return True
        return self.last_state.get("status") != new_state.get("status")

    def apply_state(self, mqtt_client, new_state: dict, manual: bool = False):
        """
        Apply the new state to the smart TV, with validation.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): New desired state. Must contain 'status'.
            manual (bool): Whether this is a manual override.
        """
        # Normalize power → status
        if "power" in new_state and "status" not in new_state:
            new_state["status"] = new_state["power"]

        if "status" not in new_state:
            raise ValueError(f"TV device requires 'status' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, manual)

