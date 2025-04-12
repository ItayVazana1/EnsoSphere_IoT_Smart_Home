"""
Module: sensors/noise_sensor.py
Purpose: Room-specific noise level sensor.
Author: Itay Vazana
"""

from sensors.sensor import Sensor


class NoiseSensor(Sensor):
    def __init__(self, sensor_id: str, room: str):
        """
        Initialize a noise sensor for a specific room.

        Args:
            sensor_id (str): Unique ID of the sensor.
            room (str): Room associated with this sensor.
        """
        super().__init__(sensor_id, room)

    def evaluate(self, state_json: dict) -> float:
        """
        Retrieves noise level for the associated room.

        Args:
            state_json (dict): Simulation state.

        Returns:
            float: Noise level in the room.
        """
        return float(state_json.get("noise_levels", {}).get(self.room, 0.0))
