"""
Module: simulator/state_builder.py
Purpose: Assemble full state_json using time, weather, and occupant data.
Author: Itay Vazana
"""

from datetime import datetime
from typing import List, Dict

from simulator.time_manager import TimeManager
from simulator.weather_engine import WeatherEngine
from simulator.occupant_engine import OccupantEngine

class StateBuilder:
    def __init__(self, time_manager: TimeManager, weather_engine: WeatherEngine, occupant_engine: OccupantEngine):
        """
        Initialize the StateBuilder with required engines.

        Args:
            time_manager (TimeManager): Time engine for simulated datetime.
            weather_engine (WeatherEngine): Weather generator.
            occupant_engine (OccupantEngine): Occupant routine handler.
        """
        self.time_manager = time_manager
        self.weather_engine = weather_engine
        self.occupant_engine = occupant_engine

    def build_state(self, character_names: List[str]) -> Dict:
        """
        Build a full state_json object for the current tick.

        Args:
            character_names (List[str]): List of active characters

        Returns:
            dict: Full state_json
        """
        current_datetime: datetime = self.time_manager.get_simulation_datetime()
        time_str = current_datetime.strftime("%H:%M")
        season = self.time_manager.get_season()
        is_daytime = self.time_manager.is_daytime()
        weather = self.weather_engine.get_weather(season)
        temperature = self.weather_engine.get_temperature(season, is_daytime)

        occupants = self.occupant_engine.get_occupant_locations(character_names, time_str)
        rooms = self.occupant_engine.get_rooms_map(occupants)

        active_rooms = [room["name"] for room in rooms if room["occupants"]]
        is_empty = len(occupants) == 0

        state = {
            "timestamp": current_datetime.isoformat(),
            "simulation_time": current_datetime.strftime("%Y-%m-%d %H:%M"),
            "season": season,
            "is_daytime": is_daytime,
            "temperature": temperature,
            "weather": weather,
            "occupants": occupants,
            "rooms": rooms,
            "house_status": {
                "is_empty": is_empty,
                "active_rooms": active_rooms
            },
            "notes": {
                "source": "simulator"
            }
        }

        return state
