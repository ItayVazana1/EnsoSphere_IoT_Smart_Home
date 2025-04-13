"""
Module: simulator/world.py
Purpose: Encapsulate global simulation conditions – time, season, weather, and outdoor temperature.
Author: Itay Vazana
"""

from simulator.engines.time_manager import TimeManager
from simulator.engines.weather_engine import WeatherEngine
from datetime import datetime


class World:
    """
    Represents the simulated world environment (time, weather, temperature).
    """

    def __init__(self, time_manager: TimeManager, weather_engine: WeatherEngine):
        self.time_manager = time_manager
        self.weather_engine = weather_engine

    def advance(self):
        """
        Advance the simulation by one tick (if supported externally).
        """
        self.time_manager.advance_tick()

    def get_datetime(self) -> datetime:
        return self.time_manager.get_simulation_datetime()

    def get_time_str(self) -> str:
        return self.get_datetime().strftime("%H:%M")

    def get_season(self) -> str:
        return self.time_manager.get_season()

    def is_daytime(self) -> bool:
        return self.time_manager.is_daytime()

    def get_weather(self) -> str:
        return self.weather_engine.get_weather(self.get_season())

    def get_outside_temperature(self) -> float:
        return self.weather_engine.get_temperature(self.get_season(), self.is_daytime())

