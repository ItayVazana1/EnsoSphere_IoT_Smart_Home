"""
Module: sensors/humidity_sensor.py
Purpose: Room-specific humidity sensor.
Author: Itay Vazana
"""

from sensors.sensor import Sensor
from typing import Any


class HumiditySensor(Sensor):
    def __init__(self, sensor_id: str, room: str, publisher=None):
        """
        Initialize a humidity sensor for a specific room.

        Args:
            sensor_id (str): Unique ID of the sensor.
            room (str): Room in which the sensor is installed.
            publisher (SensorPublisher, optional): Shared MQTT publisher instance.
        """
        super().__init__(sensor_id, room, publisher)

    def evaluate(self, state_json: dict, room_engine: Any) -> float:
        """
        Returns humidity from the room's environment.

        Args:
            state_json (dict): Simulation tick state.
            room_engine (RoomEngine): Provides room conditions.

        Returns:
            float: Simulated humidity percentage.
        """
        env = room_engine.get_environment(self.room)
        return env["humidity"] if env and "humidity" in env else 0.0
