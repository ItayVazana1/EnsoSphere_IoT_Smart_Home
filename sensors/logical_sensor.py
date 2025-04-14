"""
Module: sensors/logical_sensor.py
Purpose: Contains logical sensors derived from simulation context.
Author: Itay Vazana
"""

from sensors.sensor import Sensor
from typing import Any


class NoMotionAllRoomsSensor(Sensor):
    def __init__(self, sensor_id: str, monitored_rooms: list[str], publisher=None):
        """
        Logical sensor that evaluates True when all monitored rooms have no motion.

        Args:
            sensor_id (str): Unique ID of the logical sensor.
            monitored_rooms (list[str]): List of room names to check.
            publisher (SensorPublisher, optional): Shared MQTT publisher instance.
        """
        super().__init__(sensor_id, room=None, publisher=publisher)
        self.monitored_rooms = monitored_rooms

    def evaluate(self, state_json: dict, room_engine: Any) -> bool:
        """
        Evaluates whether all monitored rooms are inactive.

        Args:
            state_json (dict): Simulation state.
            room_engine (RoomEngine): (Unused in logical sensor)

        Returns:
            bool: True if no motion in all monitored rooms.
        """
        room_states = state_json.get("house_status", {}).get("room_state", {})
        return all(not room_states.get(room, {}).get("active", False) for room in self.monitored_rooms)
