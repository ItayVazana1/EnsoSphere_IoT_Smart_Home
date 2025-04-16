"""
Module: devices/device.py
Purpose: Defines the base Device class for all smart apartment actuators.
Author: Itay Vazana
"""

import json
from datetime import datetime
from typing import Any, Optional


class Device:
    def __init__(self, device_id: str, topic: str, metadata: Optional[dict] = None):
        """
        Initialize a device with its unique ID, MQTT topic, and metadata.

        Args:
            device_id (str): Unique identifier of the device.
            topic (str): MQTT topic to publish commands to.
            metadata (dict, optional): Metadata from device_metadata.json.
        """
        self.device_id = device_id
        self.topic = topic
        self.last_state: Optional[dict] = None
        self.metadata = metadata or {}
        self.supported_commands = self.metadata.get("supported_commands", [])
        self.optional_modes = self.metadata.get("optional_modes", [])
        self.environment_effects = self.metadata.get("environment_effects", {})

    def should_update(self, new_state: dict) -> bool:
        """
        Determines if the device should be updated based on new state.

        Args:
            new_state (dict): The desired new state to compare.

        Returns:
            bool: True if update is required, False if state is unchanged.
        """
        return self.last_state != new_state

    def apply_state(self, mqtt_client: Any, new_state: dict, state_id: Optional[int] = None, manual: bool = False):
        """
        Applies a new state to the device, only if it differs from the current state,
        or if manual override is specified.

        Args:
            mqtt_client (Any): Instance of the MQTT client used to publish commands.
            new_state (dict): New command/state to apply.
            state_id (int, optional): Tick ID for synchronization and traceability.
            manual (bool): Whether this is a manual command (bypasses state comparison).
        """
        if manual or self.should_update(new_state):
            payload = {
                "device_id": self.device_id,
                "command": new_state,
                "timestamp": datetime.utcnow().isoformat(),
                "manual": manual
            }
            if state_id is not None:
                payload["state_id"] = state_id

            mqtt_client.publish(self.topic, json.dumps(payload))
            self.last_state = new_state.copy()

    def get_environment_effect(self, command: str) -> dict:
        """
        Returns the environmental effect of a given command.

        Args:
            command (str): The command key ('on', 'off', 'cool', etc.)

        Returns:
            dict: Dictionary of affected fields and their changes.
        """
        effect = {}
        for key, command_map in self.environment_effects.items():
            if isinstance(command_map, dict) and command in command_map:
                effect[key] = command_map[command]
        return effect

    def reset_state(self):
        """
        Resets the internal last known state (used for testing or reset scenarios).
        """
        self.last_state = None
