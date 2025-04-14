"""
Module: sensors/sensor.py
Purpose: Defines the abstract base class for all sensors.
Author: Itay Vazana
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class Sensor(ABC):
    def __init__(self, sensor_id: str, room: Optional[str] = None, publisher=None):
        """
        Initialize a base sensor.

        Args:
            sensor_id (str): Unique ID of the sensor.
            room (str, optional): Room associated with the sensor, if applicable.
            publisher (SensorPublisher, optional): Shared MQTT publisher instance.
        """
        self.sensor_id = sensor_id
        self.room = room
        self.active = True
        self.last_value: Optional[Any] = None
        self.publisher = publisher  # ✅ Now passed in from outside

    @abstractmethod
    def evaluate(self, state_json: dict, room_engine: Any) -> Any:
        """
        Evaluate the sensor's value based on the simulation state and room environment.

        Args:
            state_json (dict): The current simulation state.
            room_engine (RoomEngine): Environment engine for room-specific values.

        Returns:
            Any: The sensor's output value.
        """
        pass

    def evaluate_and_store(self, state_json: dict, room_engine: Any) -> Any:
        """
        Evaluates the value, stores it internally, and publishes via MQTT if active.

        Args:
            state_json (dict): The simulation state input.
            room_engine (RoomEngine): Environmental data provider.

        Returns:
            Any: The computed sensor output.
        """
        value = self.evaluate(state_json, room_engine)
        self.last_value = value

        if self.active and self.publisher:
            self.publisher.publish_sensor_outputs({self.sensor_id: value})

        return value

    def get_id(self) -> str:
        """
        Returns the sensor's unique ID.

        Returns:
            str: Sensor ID
        """
        return self.sensor_id
