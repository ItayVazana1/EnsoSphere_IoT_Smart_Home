"""
Module: sensors/motion_sensor.py
Purpose: Motion sensor detecting activity in a specific room.
Author: Itay Vazana
"""

from sensors.sensor import Sensor
from typing import Any


class MotionSensor(Sensor):
    def __init__(self, sensor_id: str, room: str, publisher=None):
        """
        Initialize a motion sensor for a specific room.

        Args:
            sensor_id (str): Unique ID of the motion sensor.
            room (str): Room associated with this motion sensor.
            publisher (SensorPublisher, optional): Shared MQTT publisher instance.
        """
        super().__init__(sensor_id, room, publisher)

    def evaluate(self, state_json: dict, room_engine: Any) -> bool:
        """
        Evaluate motion detection based on occupants' current location.

        Args:
            state_json (dict): Current simulation state.
            room_engine (RoomEngine): (unused for motion detection)

        Returns:
            bool: True if any occupant is in the sensor's room.
        """
        occupants = state_json.get("occupants", [])
        return any(o.get("location") == self.room for o in occupants)
