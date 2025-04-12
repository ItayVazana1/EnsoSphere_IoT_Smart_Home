"""
Module: devices/device.py
Purpose: Defines the base Device class for all smart apartment actuators.
Author: Itay Vazana
"""

import json
from datetime import datetime
from typing import Any, Optional


class Device:
    def __init__(self, device_id: str, topic: str):
        """
        Initialize a device with its unique ID and associated MQTT topic.

        Args:
            device_id (str): Unique identifier of the device.
            topic (str): MQTT topic to publish commands to.
        """
        self.device_id = device_id
        self.topic = topic
        self.last_state: Optional[dict] = None  # Tracks the last known state

    def should_update(self, new_state: dict) -> bool:
        """
        Determines if the device should be updated based on new state.

        Args:
            new_state (dict): The desired new state to compare.

        Returns:
            bool: True if update is required, False if state is unchanged.
        """
        return self.last_state != new_state

    def apply_state(self, mqtt_client: Any, new_state: dict, manual: bool = False):
        """
        Applies a new state to the device, only if it differs from the current state,
        or if manual override is specified.

        Args:
            mqtt_client (Any): Instance of the MQTT client used to publish commands.
            new_state (dict): New command/state to apply.
            manual (bool): Whether this is a manual command (bypasses state comparison).
        """
        if manual or self.should_update(new_state):
            mqtt_client.publish(self.topic, json.dumps({
                "device_id": self.device_id,
                "command": new_state,
                "timestamp": datetime.utcnow().isoformat(),
                "manual": manual
            }))
            self.last_state = new_state.copy()

    def reset_state(self):
        """
        Resets the internal last known state (used for testing or reset scenarios).
        """
        self.last_state = None
