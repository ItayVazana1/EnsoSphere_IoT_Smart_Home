"""
Test: test_time_manager.py
Purpose: Unit tests for the TimeManager class
Author: Itay Vazana
"""

import pytest
from datetime import datetime
from simulator.time_manager import TimeManager

def test_initial_time():
    tm = TimeManager(start_datetime=datetime(2025, 8, 1, 6, 0))
    assert tm.get_simulation_time_string() == "2025-08-01 06:00"

def test_advance_tick():
    tm = TimeManager(start_datetime=datetime(2025, 8, 1, 6, 0))
    tm.advance_tick()
    assert tm.get_simulation_time_string() == "2025-08-01 06:30"
    tm.advance_tick()
    assert tm.get_simulation_time_string() == "2025-08-01 07:00"

def test_daytime_detection():
    tm = TimeManager(start_datetime=datetime(2025, 8, 1, 5, 0))  # 05:00
    assert tm.is_daytime() is False
    tm.advance_tick()  # 05:30
    assert tm.is_daytime() is False
    tm.advance_tick()  # 06:00
    assert tm.is_daytime() is False
    tm.advance_tick()  # 06:30
    assert tm.is_daytime() is False
    tm.advance_tick()  # 07:00
    assert tm.is_daytime() is True
    tm.advance_tick()  # 07:30
    assert tm.is_daytime() is True
    for _ in range(26):  # go to night
        tm.advance_tick()
    assert tm.is_daytime() is False  # after 20:00

def test_season_assignment():
    # Winter: Jan 15
    tm = TimeManager(start_datetime=datetime(2025, 1, 15, 6, 0))
    assert tm.get_season() == "Winter"

    # Spring: Apr 10
    tm = TimeManager(start_datetime=datetime(2025, 4, 10, 6, 0))
    assert tm.get_season() == "Spring"

    # Summer: Jul 1
    tm = TimeManager(start_datetime=datetime(2025, 7, 1, 6, 0))
    assert tm.get_season() == "Summer"

    # Autumn: Oct 20
    tm = TimeManager(start_datetime=datetime(2025, 10, 20, 6, 0))
    assert tm.get_season() == "Autumn"
