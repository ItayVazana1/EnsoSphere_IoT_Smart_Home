'''
Module: simulator/state_builder.py
Purpose: Assemble full state_json using time, weather, occupants, and sensor values, including room environmental effects.
Author: Itay Vazana
'''

import os
import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path

from simulator.time_manager import TimeManager
from simulator.weather_engine import WeatherEngine
from simulator.occupant_engine import OccupantEngine
from simulator.house_engine import HouseEngine
from simulator.room_engine import RoomEngine
from sensors.sensors_registry import load_all_sensors

sensor_map_path = Path(os.path.dirname(__file__)) / ".." / "config" / "sensor_room_map.json"

class StateBuilder:
    def __init__(self, time_manager: TimeManager, weather_engine: WeatherEngine, occupant_engine: OccupantEngine):
        self.time_manager = time_manager
        self.weather_engine = weather_engine
        self.occupant_engine = occupant_engine
        self.house_engine = HouseEngine()
        self.sensors = load_all_sensors()
        self.expected_sensor_ids = self._load_expected_sensor_ids()

    def _load_expected_sensor_ids(self) -> List[str]:
        with open(sensor_map_path, "r", encoding="utf-8") as f:
            sensor_map = json.load(f)
        return [sensor["id"] for room_sensors in sensor_map.values() for sensor in room_sensors]

    def build_state(self, character_names: List[str], device_states: Dict[str, dict]) -> Dict:
        current_datetime: datetime = self.time_manager.get_simulation_datetime()
        time_str = current_datetime.strftime("%H:%M")
        season = self.time_manager.get_season()
        is_daytime = self.time_manager.is_daytime()
        weather = self.weather_engine.get_weather(season)
        outdoor_temp = self.weather_engine.get_temperature(season, is_daytime)

        occupants = self.occupant_engine.get_occupant_locations(character_names, time_str, season)
        rooms = self.occupant_engine.get_rooms_map(occupants)

        self.house_engine.update_room_status(occupants)
        active_rooms = self.house_engine.get_active_rooms()
        room_state = self.house_engine.get_room_state()
        is_empty = len(occupants) == 0

        # Initialize RoomEngine with per-room context
        room_engine = RoomEngine(base_temperature=outdoor_temp, base_humidity=55.0)
        room_engine.init_rooms(room_state.keys())
        room_engine.apply_device_effects(device_states)

        # Build state_json with per-room context
        state = {
            "timestamp": current_datetime.isoformat(),
            "simulation_time": current_datetime.strftime("%Y-%m-%d %H:%M"),
            "season": season,
            "is_daytime": is_daytime,
            "temperature": outdoor_temp,  # global reference only
            "weather": weather,
            "occupants": occupants,
            "rooms": rooms,
            "house_status": {
                "is_empty": is_empty,
                "active_rooms": active_rooms,
                "room_state": room_state
            },
            "notes": {
                "source": "simulator"
            }
        }

        # Evaluate all sensors using local room_engine context
        sensor_outputs = {}
        sensor_lookup = {s.get_id(): s for s in self.sensors}

        for sensor_id in self.expected_sensor_ids:
            sensor = sensor_lookup.get(sensor_id)
            if sensor:
                try:
                    sensor_outputs[sensor_id] = sensor.evaluate_and_store(state, room_engine)
                except Exception as e:
                    print(f"⚠️ Sensor {sensor_id} evaluation failed: {e}")
                    sensor_outputs[sensor_id] = None
            else:
                print(f"⚠️ Sensor {sensor_id} not implemented. Setting value to None.")
                sensor_outputs[sensor_id] = None

        state["sensors"] = sensor_outputs
        return state
