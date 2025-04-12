"""
Module: sensors/gas_sensor.py
Purpose: Global gas level sensor.
Author: Itay Vazana
"""

from sensors.sensor import Sensor


class GasSensor(Sensor):
    def __init__(self, sensor_id: str):
        """
        Initialize a gas sensor (global).

        Args:
            sensor_id (str): Unique ID of the gas sensor.
        """
        super().__init__(sensor_id)

    def evaluate(self, state_json: dict) -> float:
        """
        Retrieves the gas level from the simulation state.

        Args:
            state_json (dict): Current tick simulation state.

        Returns:
            float: The gas level value.
        """
        return float(state_json.get("gas", 0.0))
