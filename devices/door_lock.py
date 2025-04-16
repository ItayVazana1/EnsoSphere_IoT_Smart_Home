"""
Module: devices/door_lock.py
Purpose: Smart door lock device that manages lock/unlock states.
Author: Itay Vazana
"""

from devices.device import Device


class DoorLock(Device):
    def __init__(self, device_id: str, metadata: dict):
        """
        Initialize a smart Door Lock device.

        Args:
            device_id (str): Unique ID of the Door Lock device.
            metadata (dict): Metadata for this device type from device_metadata.json
        """
        super().__init__(device_id, topic=f"actuators/{device_id}", metadata=metadata)

    def should_update(self, new_state: dict) -> bool:
        """
        Compare 'locked' field to determine if update is required.

        Args:
            new_state (dict): New desired state for the door lock.

        Returns:
            bool: True if lock state changed, False otherwise.
        """
        if not self.last_state:
            return True
        return self.last_state.get("locked") != new_state.get("locked")

    def apply_state(self, mqtt_client, new_state: dict, state_id: int = None, manual: bool = False):
        """
        Apply the new lock state to the smart door lock.

        Args:
            mqtt_client: MQTT client instance.
            new_state (dict): Must contain 'locked' key (True/False) or status (lock/unlock).
            state_id (int): Tick ID for traceability.
            manual (bool): Whether this is a manual override.
        """
        # Normalize command to 'locked'
        if "locked" not in new_state:
            if new_state.get("status") == "lock":
                new_state["locked"] = True
            elif new_state.get("status") == "unlock":
                new_state["locked"] = False

        if "locked" not in new_state:
            raise ValueError(f"DoorLock requires 'locked' boolean or lock/unlock status: {new_state}")

        super().apply_state(mqtt_client, new_state, state_id=state_id, manual=manual)
