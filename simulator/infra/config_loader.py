"""
Module: simulator/config_loader.py
Purpose: Utility functions for loading JSON configuration files like sensor maps.
Author: Itay Vazana
"""

import json
from pathlib import Path

def load_sensor_map() -> dict:
    """
    Loads the sensor_room_map.json file from the config directory.

    Returns:
        dict: room_name → list of sensor dicts
    """
    path = Path(__file__).parent.parent / "config" / "sensor_room_map.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
