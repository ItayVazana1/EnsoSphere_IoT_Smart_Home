"""
Module: sensors/sensor.py
Purpose: Defines the abstract base class for all sensors.
Author: Itay Vazana
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class Sensor(ABC):
    def __init__(self, sensor_id: str, room: Optional[str] = None):
        """
        Initialize a base sensor.

        Args:
            sensor_id (str): Unique ID of the sensor.
            room (str, optional): Room associated with the sensor, if applicable.
        """
        self.sensor_id = sensor_id
        self.room = room
        self.last_value: Optional[Any] = None

    @abstractmethod
    def evaluate(self, state_json: dict) -> Any:
        """
        Evaluate the sensor's value based on the given simulation state.

        Args:
            state_json (dict): The state JSON object for the current tick.

        Returns:
            Any: The sensor's output value.
        """
        pass

    def evaluate_and_store(self, state_json: dict) -> Any:
        """
        Evaluates and stores the result for internal tracking.

        Args:
            state_json (dict): The simulation state input.

        Returns:
            Any: The computed sensor output.
        """
        value = self.evaluate(state_json)
        self.last_value = value
        return value
