"""
Module: corelogic/sensor_manager.py
Purpose: Evaluates all sensors based on state_json.
Author: Itay Vazana
"""

from sensors.sensors_registry import get_all_sensors


class SensorManager:
    def __init__(self):
        """
        Initializes the sensor manager and loads all available sensors.
        """
        self.sensors = get_all_sensors()

    def evaluate_sensors(self, state_json: dict) -> dict:
        """
        Evaluates all sensors against the current simulation state.

        Args:
            state_json (dict): The simulator-generated state for this tick.

        Returns:
            dict: Mapping from sensor_id to evaluated value.
        """
        outputs = {}
        for sensor in self.sensors:
            if sensor.active:  # ✅ Only process active sensors
                value = sensor.evaluate_and_store(state_json)
                outputs[sensor.sensor_id] = value
        return outputs
