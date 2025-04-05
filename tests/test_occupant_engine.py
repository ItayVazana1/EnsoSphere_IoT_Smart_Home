"""
Test: test_occupant_engine.py
Purpose: Validate full routine loading and logic for occupant location and room map
Author: Itay Vazana
"""

import pytest
from pathlib import Path
from simulator.occupant_engine import OccupantEngine

# Resolve full path to routines/ so tests run from anywhere
ROUTINES_DIR = "../routines/"

def test_full_routine_parsing():
    engine = OccupantEngine(season="Summer", routines_dir=ROUTINES_DIR)
    character = "Testy"

    # Loop through all 48 expected half-hour time slots
    time_slots = [f"{h:02d}:{m:02d}" for h in list(range(6, 24)) + list(range(0, 6)) for m in [0, 30]]

    for time in time_slots:
        location = engine.get_character_location(character, time)
        print(f"[{time}] {character} → {location}")
        assert isinstance(location, str), f"Returned location is not a string at {time}"
        assert len(location) > 0, f"Empty location string at {time}"

def test_room_mapping():
    engine = OccupantEngine(season="Summer", routines_dir=ROUTINES_DIR)
    time = "07:30"  # Should be Balcony in Summer
    occupants = engine.get_occupant_locations(["Testy"], time)
    print(f"Room mapping at {time}: {occupants}")
    assert occupants == [{'name': 'Testy', 'location': 'Balcony'}]

    rooms = engine.get_rooms_map(occupants)
    print(f"Rooms → {rooms}")
    assert rooms == [{'name': 'Balcony', 'occupants': ['Testy']}]



