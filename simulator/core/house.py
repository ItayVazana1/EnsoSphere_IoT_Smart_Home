"""
Module: simulator/house.py
Purpose: Manage the full structure and state of the smart apartment including rooms and occupants.
Author: Itay Vazana
"""

from simulator.core.room import Room
from simulator.engines.occupant_engine import OccupantEngine
from sensors.sensor import Sensor
from typing import Dict, List, Optional


class House:
    """
    The House class manages all Room objects and current occupant locations.
    It handles:
    - Occupant tracking (via OccupantEngine)
    - Device influence per room
    - Room environment updates
    - Sensor outputs
    - System-level summaries
    """

    def __init__(self, sensor_map: Dict[str, List[Sensor]], routines_dir: str = "routines/"):
        """
        Initialize rooms and occupant engine.

        Args:
            sensor_map (Dict): room_name → list of Sensor objects
            routines_dir (str): path to Excel routine files
        """
        self.rooms: Dict[str, Room] = {}

        for room_name, sensor_list in sensor_map.items():
            self.rooms[room_name] = Room(name=room_name, sensors=sensor_list)

        self.occupant_engine = OccupantEngine(routines_dir)
        self.current_occupants: List[Dict] = []

    def update_occupants_by_time(self, characters: List[str], time_str: str, season: str):
        """
        Load current occupant locations from routine files and mark active rooms.
        """
        self.current_occupants = self.occupant_engine.get_occupant_locations(characters, time_str, season)
        active_rooms = {o["location"] for o in self.current_occupants}
        for name, room in self.rooms.items():
            room.active = name in active_rooms

    def update_devices(self, device_states: Dict[str, dict]):
        """
        Apply device states to rooms. Actual effects applied later via apply_all_device_effects().
        """
        for device_id, state in device_states.items():
            # Global devices (e.g., robot vacuum) affect all rooms
            if "robot_vacuum" in device_id:
                for room in self.rooms.values():
                    room.apply_device_state(device_id, state)
                continue

            matched_room = self._extract_room_from_id(device_id)
            if matched_room:
                matched_room.apply_device_state(device_id, state)

    def update_environment(self, outside_temp: float):
        """
        Propagate environment updates to all rooms.
        """
        for room in self.rooms.values():
            room.update_environment(outside_temp)

    def generate_sensor_outputs(self, state_json: dict = None) -> Dict[str, float]:
        """
        Collect sensor outputs from all rooms.
        """
        outputs = {}
        for room in self.rooms.values():
            room_outputs = room.generate_sensor_outputs(state_json or {}, self)
            outputs.update(room_outputs)
        return outputs

    def get_environment(self, room_name: str) -> dict:
        """
        Returns the environmental values of a specific room.
        """
        room = self.rooms.get(room_name)
        return room.get_environment() if room else {}

    def get_room_map(self) -> List[Dict]:
        return self.occupant_engine.get_rooms_map(self.current_occupants)

    def get_occupants(self) -> List[Dict]:
        return self.current_occupants

    def get_active_rooms(self) -> List[str]:
        return [name for name, room in self.rooms.items() if room.active]

    def get_room_states(self) -> Dict[str, Dict]:
        return {
            name: {
                "active": room.active,
                "env": room.get_environment()
            }
            for name, room in self.rooms.items()
        }

    def get_room(self, room_name: str) -> Optional[Room]:
        return self.rooms.get(room_name)

    def get_all_rooms(self) -> Dict[str, Room]:
        return self.rooms

    def get_room_by_sensor(self, sensor_id: str) -> Optional[Room]:
        for room in self.rooms.values():
            if room.has_sensor(sensor_id):
                return room
        return None

    def reset_all_rooms(self):
        """
        Calls the reset_state method on every room.
        """
        for room in self.rooms.values():
            room.reset_state()

    def get_summary(self) -> Dict[str, float]:
        temps, hums, noises = [], [], []
        for room in self.rooms.values():
            env = room.get_environment()
            temps.append(env["temperature"])
            hums.append(env["humidity"])
            noises.append(env["noise"])

        def avg(values: List[float]) -> float:
            return round(sum(values) / len(values), 1) if values else 0.0

        return {
            "avg_temperature": avg(temps),
            "avg_humidity": avg(hums),
            "avg_noise": avg(noises),
            "active_rooms": len(self.get_active_rooms()),
            "total_rooms": len(self.rooms)
        }

    def _extract_room_from_id(self, device_id: str) -> Optional[Room]:
        if "_" not in device_id:
            return None
        suffix = device_id.split("_", 1)[-1]
        for name, room in self.rooms.items():
            if name.lower().endswith(suffix.lower()):
                return room
        return None
