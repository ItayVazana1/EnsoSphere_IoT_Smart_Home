"""
Module: devices/air_conditioner.py
Purpose: Air Conditioner device with support for on/off and temperature settings.
Author: Itay Vazana
"""

from devices.device import Device


class AirConditioner(Device):
    def __init__(self, device_id: str, metadata: dict):
        """
        Initialize a smart Air Conditioner device.

        Args:
            device_id (str): Unique ID of the AC device.
            metadata (dict): Metadata for this device type from device_metadata.json
        """
        super().__init__(device_id, topic=f"actuators/{device_id}", metadata=metadata)

    def should_update(self, new_state: dict) -> bool:
        """
        Compares 'status' and 'mode' for determining state change.

        Args:
            new_state (dict): New desired state.

        Returns:
            bool: True if update needed, False otherwise.
        """
        if not self.last_state:
            return True
        return any([
            self.last_state.get("status") != new_state.get("status"),
            self.last_state.get("mode") != new_state.get("mode")
        ])

    def apply_state(self, mqtt_client, new_state: dict, state_id: int = None, manual: bool = False):
        """
        Apply new AC state with required field validation.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): State dict with at least 'status'.
            state_id (int): Simulation tick ID for tracking.
            manual (bool): Whether this is a manual override.
        """
        if "status" not in new_state:
            raise ValueError(f"AirConditioner requires 'status' in command: {new_state}")

        # Add mode if needed
        if new_state["status"] == "on" and "mode" not in new_state:
            new_state["mode"] = "cool"
        elif new_state["status"] == "off":
            new_state["mode"] = "off"

        # Call base method with state_id
        super().apply_state(mqtt_client, new_state, state_id=state_id, manual=manual)

    def get_temperature_effect(self) -> float:
        """
        Returns the temperature delta caused by the current mode (if any).

        Returns:
            float: Temperature change value (e.g., -0.8 for cool).
        """
        if not self.last_state:
            return 0.0
        mode = self.last_state.get("mode")
        effect = self.get_environment_effect(mode)
        return effect.get("temperature", 0.0)
