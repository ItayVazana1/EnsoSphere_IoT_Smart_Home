"""
Module: devices/audio_system.py
Purpose: Audio system device with basic on/off and validation.
Author: Itay Vazana
"""

from devices.device import Device


class AudioSystem(Device):
    def __init__(self, device_id: str):
        """
        Initialize a smart Audio System device.

        Args:
            device_id (str): Unique ID of the AudioSystem device.
        """
        super().__init__(device_id, topic=f"actuators/{device_id}")

    def should_update(self, new_state: dict) -> bool:
        """
        Overrides base logic to compare only the 'status' field for AudioSystem.

        Args:
            new_state (dict): New desired state for the Audio System.

        Returns:
            bool: True if status has changed, False otherwise.
        """
        if not self.last_state:
            return True
        return self.last_state.get("status") != new_state.get("status")

    def apply_state(self, mqtt_client, new_state: dict, manual: bool = False):
        """
        Apply the new state to the Audio System, with validation.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): New desired state. Must contain 'status'.
            manual (bool): Whether this is a manual override.
        """
        # Normalize "on"/"off" to explicit status if needed
        if "power" in new_state and "status" not in new_state:
            new_state["status"] = new_state["power"]

        if "status" not in new_state:
            raise ValueError(f"AudioSystem device requires 'status' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, manual)
