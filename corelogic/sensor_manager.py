"""
Module: corelogic/sensor_manager.py
Purpose: Extract and compute sensor output values from state_json during each simulation tick.
Author: Itay Vazana
"""

from typing import Dict, Any
import json

class SensorManager:
    def __init__(self):
        """
        Initialize SensorManager. No dynamic config required for now.
        """
        pass

    def evaluate_sensors(self, state_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Given a full state_json from the simulator, compute the value of each virtual sensor.

        Args:
            state_json (dict): The full tick state, including occupant locations, environment, etc.

        Returns:
            dict: Dictionary of {sensor_id: value} pairs.
        """
        sensor_outputs = {}

        # 1. Occupancy-based motion sensors
        for room in state_json.get("room_states", {}):
            is_active = state_json["room_states"][room] == "Active"
            sensor_id = f"motion_{room.lower()}"
            sensor_outputs[sensor_id] = is_active

        # 2. Environmental sensors
        sensor_outputs["temperature"] = state_json.get("temperature")
        sensor_outputs["weather"] = state_json.get("weather")
        sensor_outputs["is_daytime"] = state_json.get("is_daytime")
        sensor_outputs["season"] = state_json.get("season")

        # 3. Logical sensor: no_motion_all_rooms
        motion_values = [v for k, v in sensor_outputs.items() if k.startswith("motion_")]
        sensor_outputs["no_motion_all_rooms"] = not any(motion_values)

        return sensor_outputs
