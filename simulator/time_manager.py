"""
Module: simulator/time_manager.py
Purpose: Manage accelerated simulated time and derive simulation date, time, season, and daylight flag.
Author: Itay Vazana
"""

from datetime import datetime, timedelta

class TimeManager:
    def __init__(self, start_datetime: datetime, tick_interval_minutes: int = 30):
        """
        Initialize the TimeManager.

        Args:
            start_datetime (datetime): The initial simulated datetime.
            tick_interval_minutes (int): Simulated minutes per tick (default 30).
        """
        self.start_datetime = start_datetime
        self.tick_interval = timedelta(minutes=tick_interval_minutes)
        self.current_tick = 0

    def advance_tick(self) -> None:
        """
        Advance the simulated clock by one tick.
        """
        self.current_tick += 1

    def get_simulation_datetime(self) -> datetime:
        """
        Get the current simulated datetime.

        Returns:
            datetime: The current simulated time.
        """
        return self.start_datetime + self.tick_interval * self.current_tick

    def get_simulation_time_string(self) -> str:
        """
        Get the current simulation time in string format.

        Returns:
            str: Formatted simulation time (YYYY-MM-DD HH:MM).
        """
        return self.get_simulation_datetime().strftime("%Y-%m-%d %H:%M")

    def get_season(self) -> str:
        """
        Determine the current season based on the month.

        Returns:
            str: One of ['Winter', 'Spring', 'Summer', 'Autumn']
        """
        month = self.get_simulation_datetime().month
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"

    def is_daytime(self) -> bool:
        """
        Determine if the current simulation time is daytime.

        Returns:
            bool: True if between 07:00 and 20:00, False otherwise.
        """
        hour = self.get_simulation_datetime().hour
        return 7 <= hour < 20
