"""
Module: simulator/weather_engine.py
Purpose: Generate weather and temperature values based on season and day/night status.
Author: Itay Vazana
"""

import random

class WeatherEngine:
    def __init__(self):
        # Weather probability map by season
        self.weather_probabilities = {
            "Summer": {"Sunny": 0.7, "Cloudy": 0.2, "Rainy": 0.1},
            "Winter": {"Sunny": 0.2, "Cloudy": 0.3, "Rainy": 0.5},
            "Spring": {"Sunny": 0.5, "Cloudy": 0.3, "Rainy": 0.2},
            "Autumn": {"Sunny": 0.4, "Cloudy": 0.4, "Rainy": 0.2}
        }

        # Base temperature ranges (°C) per season
        self.temperature_ranges = {
            "Summer": (27, 35),
            "Winter": (5, 15),
            "Spring": (15, 24),
            "Autumn": (12, 22)
        }

    def get_weather(self, season: str) -> str:
        """
        Choose a weather condition based on seasonal probabilities.

        Args:
            season (str): Current season

        Returns:
            str: One of 'Sunny', 'Cloudy', 'Rainy'
        """
        choices = list(self.weather_probabilities[season].items())
        conditions, weights = zip(*choices)
        return random.choices(conditions, weights=weights, k=1)[0]

    def get_temperature(self, season: str, is_daytime: bool) -> float:
        """
        Generate a temperature value based on season and time of day.

        Args:
            season (str): Current season
            is_daytime (bool): Whether it's daytime

        Returns:
            float: Simulated temperature in °C
        """
        min_temp, max_temp = self.temperature_ranges[season]
        base_temp = random.uniform(min_temp, max_temp)

        # Apply slight day/night adjustment
        if not is_daytime:
            base_temp -= random.uniform(1.5, 3.0)

        return round(base_temp, 1)
