"""
Module: sensors/logical_sensor.py
Purpose: Contains logical sensors derived from simulation context.
Author: Itay Vazana
"""

from sensors.sensor import Sensor


class NoMotionAllRoomsSensor(Sensor):
    def __init__(self, sensor_id: str, monitored_rooms: list[str]):
        """
        Logical sensor that evaluates True when all monitored rooms have no motion.

        Args:
            sensor_id (str): Unique ID of the logical sensor.
            monitored_rooms (list[str]): List of room names to check.
        """
        super().__init__(sensor_id)
        self.monitored_rooms = monitored_rooms

    def evaluate(self, state_json: dict) -> bool:
        """
        Evaluates whether all monitored rooms are inactive.

        Args:
            state_json (dict): Simulation state.

        Returns:
            bool: True if no motion in all monitored rooms.
        """
        room_states = state_json.get("room_states", {})
        return all(room_states.get(room) != "Active" for room in self.monitored_rooms)
