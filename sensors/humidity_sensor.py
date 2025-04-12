"""
Module: sensors/humidity_sensor.py
Purpose: Global humidity sensor.
Author: Itay Vazana
"""

from sensors.sensor import Sensor


class HumiditySensor(Sensor):
    def __init__(self, sensor_id: str):
        """
        Initialize a humidity sensor (global).

        Args:
            sensor_id (str): Unique ID of the sensor.
        """
        super().__init__(sensor_id)

    def evaluate(self, state_json: dict) -> float:
        """
        Retrieves the global humidity value from the simulation state.

        Args:
            state_json (dict): Current tick simulation state.

        Returns:
            float: The humidity value.
        """
        return float(state_json.get("humidity", 0.0))
