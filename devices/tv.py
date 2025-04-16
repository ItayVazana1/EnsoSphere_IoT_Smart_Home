"""
Module: devices/tv.py
Purpose: Smart TV device with specific behavior for on/off states.
Author: Itay Vazana
"""

from devices.device import Device


class TV(Device):
    def __init__(self, device_id: str, metadata: dict):
        """
        Initialize a smart TV device.

        Args:
            device_id (str): Unique ID of the TV device.
            metadata (dict): Metadata for this device type from device_metadata.json
        """
        super().__init__(device_id, topic=f"actuators/{device_id}", metadata=metadata)

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

    def apply_state(self, mqtt_client, new_state: dict, state_id: int = None, manual: bool = False):
        """
        Apply the new state to the smart TV, with validation.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must contain 'status'.
            state_id (int): Tick ID for traceability.
            manual (bool): Whether this is a manual override.
        """
        if "power" in new_state and "status" not in new_state:
            new_state["status"] = new_state["power"]

        if "status" not in new_state:
            raise ValueError(f"TV device requires 'status' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, state_id=state_id, manual=manual)

    def get_noise_effect(self) -> float:
        """
        Returns the noise level effect caused by current TV status.

        Returns:
            float: Noise change value.
        """
        if not self.last_state:
            return 0.0
        status = self.last_state.get("status")
        effect = self.get_environment_effect(status)
        return effect.get("noise", 0.0)
