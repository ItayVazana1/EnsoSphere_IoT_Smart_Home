"""
Module: devices/ventilation_fan.py
Purpose: Ventilation fan device for air circulation in bathrooms.
Author: Itay Vazana
"""

from devices.device import Device


class VentilationFan(Device):
    def __init__(self, device_id: str, metadata: dict):
        """
        Initialize a smart ventilation fan device.

        Args:
            device_id (str): Unique ID of the ventilation fan.
            metadata (dict): Metadata for this device type from device_metadata.json
        """
        super().__init__(device_id, topic=f"actuators/{device_id}", metadata=metadata)

    def should_update(self, new_state: dict) -> bool:
        """
        Compare 'status' field to detect fan state change.

        Args:
            new_state (dict): Desired command.

        Returns:
            bool: True if 'status' changed.
        """
        if not self.last_state:
            return True
        return self.last_state.get("status") != new_state.get("status")

    def apply_state(self, mqtt_client, new_state: dict, state_id: int = None, manual: bool = False):
        """
        Apply the new state to the ventilation fan with validation.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must contain 'status'.
            state_id (int): Tick ID for traceability.
            manual (bool): Whether this is a manual override.
        """
        if "power" in new_state and "status" not in new_state:
            new_state["status"] = new_state["power"]

        if "status" not in new_state:
            raise ValueError(f"VentilationFan requires 'status' in command: {new_state}")

        super().apply_state(mqtt_client, new_state, state_id=state_id, manual=manual)

    def get_humidity_effect(self) -> float:
        """
        Returns the humidity change caused by the fan state.

        Returns:
            float: Humidity delta (e.g., -5.0 when on).
        """
        if not self.last_state:
            return 0.0
        status = self.last_state.get("status")
        effect = self.get_environment_effect(status)
        return effect.get("humidity", 0.0)
