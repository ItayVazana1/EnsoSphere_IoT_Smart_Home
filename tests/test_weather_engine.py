"""
Test: test_weather_engine.py
Purpose: Unit tests for the WeatherEngine class
Author: Itay Vazana
"""

import pytest
from simulator.weather_engine import WeatherEngine

def test_weather_output_validity():
    we = WeatherEngine()
    valid_conditions = {"Sunny", "Cloudy", "Rainy"}

    for season in ["Summer", "Winter", "Spring", "Autumn"]:
        for _ in range(100):
            weather = we.get_weather(season)
            assert weather in valid_conditions, f"Invalid weather: {weather} for season: {season}"

def test_temperature_range_daytime():
    we = WeatherEngine()
    for season, (min_temp, max_temp) in we.temperature_ranges.items():
        for _ in range(50):
            temp = we.get_temperature(season, is_daytime=True)
            assert min_temp <= temp <= max_temp, f"{season} daytime temp {temp} out of range {min_temp}-{max_temp}"

def test_temperature_range_nighttime():
    we = WeatherEngine()
    for season, (min_temp, max_temp) in we.temperature_ranges.items():
        for _ in range(50):
            temp = we.get_temperature(season, is_daytime=False)
            adjusted_min = min_temp - 3.0
            assert adjusted_min <= temp <= max_temp, f"{season} night temp {temp} out of range {adjusted_min}-{max_temp}"
