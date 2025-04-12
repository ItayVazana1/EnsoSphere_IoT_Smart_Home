"""
Module: sensors/motion_sensor.py
Purpose: Motion sensor detecting activity in a specific room.
Author: Itay Vazana
"""

from sensors.sensor import Sensor


class MotionSensor(Sensor):
    def __init__(self, sensor_id: str, room: str):
        """
        Initialize a motion sensor for a specific room.

        Args:
            sensor_id (str): Unique ID of the motion sensor.
            room (str): Room associated with this motion sensor.
        """
        super().__init__(sensor_id, room)

    def evaluate(self, state_json: dict) -> bool:
        """
        Evaluate motion detection based on room activity in state_json.

        Args:
            state_json (dict): Current simulation state.

        Returns:
            bool: True if the room is 'Active', otherwise False.
        """
        return state_json.get("room_states", {}).get(self.room) == "Active"
