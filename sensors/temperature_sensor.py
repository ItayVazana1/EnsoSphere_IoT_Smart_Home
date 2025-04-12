"""
Module: sensors/temperature_sensor.py
Purpose: Global temperature sensor.
Author: Itay Vazana
"""

from sensors.sensor import Sensor


class TemperatureSensor(Sensor):
    def __init__(self, sensor_id: str):
        """
        Initialize a temperature sensor (global).

        Args:
            sensor_id (str): Unique ID of the sensor.
        """
        super().__init__(sensor_id)

    def evaluate(self, state_json: dict) -> float:
        """
        Retrieves the global temperature from the simulation state.

        Args:
            state_json (dict): Current tick simulation state.

        Returns:
            float: The temperature value.
        """
        return float(state_json.get("temperature", 0.0))
