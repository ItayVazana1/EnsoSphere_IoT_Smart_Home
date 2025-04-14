"""
Module: sensors/noise_sensor.py
Purpose: Room-specific noise level sensor.
Author: Itay Vazana
"""

from sensors.sensor import Sensor
from typing import Any


class NoiseSensor(Sensor):
    def __init__(self, sensor_id: str, room: str, publisher=None):
        """
        Initialize a noise sensor for a specific room.

        Args:
            sensor_id (str): Unique ID of the sensor.
            room (str): Room associated with this sensor.
            publisher (SensorPublisher, optional): Shared MQTT publisher instance.
        """
        super().__init__(sensor_id, room, publisher)

    def evaluate(self, state_json: dict, room_engine: Any) -> float:
        """
        Retrieves noise level for the associated room from room environment.

        Args:
            state_json (dict): Simulation state.
            room_engine (RoomEngine): Room environment data.

        Returns:
            float: Noise level in the room.
        """
        env = room_engine.get_environment(self.room)
        return env["noise"] if env and "noise" in env else 0.0
