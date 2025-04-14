"""
Module: sensors/temperature_sensor.py
Purpose: Room-based temperature sensor.
Author: Itay Vazana
"""

from sensors.sensor import Sensor
from typing import Any


class TemperatureSensor(Sensor):
    def __init__(self, sensor_id: str, room: str, publisher=None):
        """
        Initialize a temperature sensor for a specific room.

        Args:
            sensor_id (str): Unique ID of the sensor.
            room (str): Room this temperature sensor is located in.
            publisher (SensorPublisher, optional): Shared MQTT publisher instance.
        """
        super().__init__(sensor_id, room, publisher)

    def evaluate(self, state_json: dict, room_engine: Any) -> float:
        """
        Retrieves the temperature value for the given room from RoomEngine.

        Args:
            state_json (dict): Current tick simulation state.
            room_engine (RoomEngine): Engine managing room conditions.

        Returns:
            float: Room temperature.
        """
        env = room_engine.get_environment(self.room)
        return env["temperature"] if env and "temperature" in env else 0.0
