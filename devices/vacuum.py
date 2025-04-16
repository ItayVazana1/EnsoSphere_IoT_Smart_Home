"""
Module: devices/vacuum.py
Purpose: Robot vacuum cleaner device for autonomous cleaning.
Author: Itay Vazana
"""

from devices.device import Device


class RobotVacuum(Device):
    def __init__(self, device_id: str, metadata: dict):
        """
        Initialize a smart robot vacuum device.

        Args:
            device_id (str): Unique ID of the robot vacuum device.
            metadata (dict): Metadata for this device type from device_metadata.json
        """
        super().__init__(device_id, topic=f"actuators/{device_id}", metadata=metadata)

    def should_update(self, new_state: dict) -> bool:
        """
        Compare 'status' to determine if vacuum needs activation.

        Args:
            new_state (dict): Desired vacuum state.

        Returns:
            bool: True if state has changed.
        """
        if not self.last_state:
            return True
        return self.last_state.get("status") != new_state.get("status")

    def apply_state(self, mqtt_client, new_state: dict, state_id: int = None, manual: bool = False):
        """
        Apply new vacuum state with validation.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must include 'status' (start_cleaning/stop).
            state_id (int): Tick ID for traceability.
            manual (bool): Whether this is a manual override.
        """
        # Normalize common variants to supported values
        if "status" not in new_state:
            if new_state.get("power") == "on":
                new_state["status"] = "start_cleaning"
            elif new_state.get("power") == "off":
                new_state["status"] = "stop"
            elif new_state.get("mode") in ("start", "clean"):
                new_state["status"] = "start_cleaning"

        if "status" not in new_state:
            raise ValueError(f"RobotVacuum requires 'status' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, state_id=state_id, manual=manual)

    def get_noise_effect(self) -> float:
        """
        Returns the noise level effect caused by vacuum operation.

        Returns:
            float: Noise delta caused by current status.
        """
        if not self.last_state:
            return 0.0
        status = self.last_state.get("status")
        effect = self.get_environment_effect(status)
        return effect.get("noise", 0.0)
