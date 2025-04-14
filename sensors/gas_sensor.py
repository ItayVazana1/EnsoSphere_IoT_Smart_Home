"""
Module: sensors/gas_sensor.py
Purpose: Gas level sensor (room-specific).
Author: Itay Vazana
"""

from sensors.sensor import Sensor
from typing import Any
import random


class GasSensor(Sensor):
    def __init__(self, sensor_id: str, room: str, publisher=None):
        """
        Initialize a gas sensor for a specific room.

        Args:
            sensor_id (str): Unique ID of the gas sensor.
            room (str): Room in which the sensor is installed.
            publisher (SensorPublisher, optional): Shared MQTT publisher instance.
        """
        super().__init__(sensor_id, room, publisher)

    def evaluate(self, state_json: dict, room_engine: Any) -> float:
        """
        Simulate gas level in the given room. Currently, returns a fixed safe value.

        Args:
            state_json (dict): Simulation tick state.
            room_engine (RoomEngine): Room environment manager.

        Returns:
            float: Gas level (0.0 to 10.0 scale).
        """
        env = room_engine.get_environment(self.room)
        if env is None:
            return 0.0

        # Simulate slight fluctuation near 0 (safe)
        return round(random.uniform(0.0, 0.3), 2)
