"""
Module: devices/light.py
Purpose: Smart Light device with basic on/off control.
Author: Itay Vazana
"""

from devices.device import Device


class Light(Device):
    def __init__(self, device_id: str, metadata: dict):
        """
        Initialize a smart Light device.

        Args:
            device_id (str): Unique ID of the Light device.
            metadata (dict): Metadata for this device type from device_metadata.json
        """
        super().__init__(device_id, topic=f"actuators/{device_id}", metadata=metadata)

    def should_update(self, new_state: dict) -> bool:
        """
        Compare 'status' field to determine if update is required.

        Args:
            new_state (dict): New desired state for the Light.

        Returns:
            bool: True if status has changed, False otherwise.
        """
        if not self.last_state:
            return True
        return self.last_state.get("status") != new_state.get("status")

    def apply_state(self, mqtt_client, new_state: dict, state_id: int = None, manual: bool = False):
        """
        Apply the new state to the Light device.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must contain 'status' key.
            state_id (int): Tick ID for traceability.
            manual (bool): Whether this is a manual override.
        """
        if "power" in new_state and "status" not in new_state:
            new_state["status"] = new_state["power"]

        if "status" not in new_state:
            raise ValueError(f"Light device requires 'status' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, state_id=state_id, manual=manual)

    def get_noise_effect(self) -> float:
        """
        Returns the noise level effect caused by current light state.

        Returns:
            float: Noise change value.
        """
        if not self.last_state:
            return 0.0
        status = self.last_state.get("status")
        effect = self.get_environment_effect(status)
        return effect.get("noise", 0.0)
