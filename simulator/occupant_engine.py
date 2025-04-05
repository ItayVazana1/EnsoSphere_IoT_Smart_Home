"""
Module: simulator/occupant_engine.py
Purpose: Load and interpret character routines per season and return occupant + room mapping.
Author: Itay Vazana
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict

class OccupantEngine:
    def __init__(self, season: str, routines_dir: str = "routines/"):
        """
        Initialize the occupant engine.

        Args:
            season (str): Current simulation season.
            routines_dir (str): Path to folder containing routine files.
        """
        self.season = season
        self.routines_dir = Path(routines_dir)
        self.cache = {}  # Cache loaded DataFrames by character

    def get_character_location(self, character: str, time_str: str) -> str:
        """
        Get a character's location at a given time and season.

        Args:
            character (str): Name of the character (matches filename).
            time_str (str): Simulation time in HH:MM format (e.g., "07:30").

        Returns:
            str: Room or location (e.g., 'Kitchen', 'Work')
        """
        df = self._load_routine(character)
        row = df[df["Time"] == time_str]
        if row.empty:
            raise ValueError(f"Time '{time_str}' not found in routine for {character}")
        return row.iloc[0][self.season]

    def get_occupant_locations(self, characters: List[str], time_str: str) -> List[Dict]:
        """
        Returns full list of occupants and their current locations.

        Args:
            characters (list): Character names
            time_str (str): Time in HH:MM format

        Returns:
            list[dict]: e.g., [{'name': 'Testy', 'location': 'Bathroom'}, ...]
        """
        return [
            {"name": name, "location": self.get_character_location(name, time_str)}
            for name in characters
        ]

    def get_rooms_map(self, occupants: List[Dict]) -> List[Dict]:
        """
        Convert list of occupants into room-wise structure.

        Args:
            occupants (list): Output from get_occupant_locations

        Returns:
            list[dict]: [{'name': 'Kitchen', 'occupants': ['Testy']}]
        """
        room_map = {}
        for o in occupants:
            room = o["location"]
            if room not in room_map:
                room_map[room] = []
            room_map[room].append(o["name"])

        return [{"name": room, "occupants": names} for room, names in room_map.items()]

    def _load_routine(self, character: str) -> pd.DataFrame:
        """
        Loads and caches the routine Excel file for a character.

        Args:
            character (str): Character name (e.g., 'Testy')

        Returns:
            pd.DataFrame: Parsed routine file
        """
        if character in self.cache:
            return self.cache[character]

        path = self.routines_dir / f"{character}.xlsx"
        if not path.exists():
            raise FileNotFoundError(f"Routine file not found: {path}")

        df = pd.read_excel(path)
        if "Time" not in df.columns or self.season not in df.columns:
            raise ValueError(f"Routine file missing required columns: {path}")

        self.cache[character] = df
        return df
