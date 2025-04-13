"""
Module: simulator/room_engine.py
Purpose: Manage per-room environmental state and compute effects of device activity.
Author: Itay Vazana
"""

from typing import Dict, Optional


class RoomEngine:
    def __init__(self, base_temperature: float, base_humidity: float):
        """
        Initialize with base temperature and humidity (from weather engine).
        """
        self.base_temp = base_temperature
        self.base_humidity = base_humidity
        self.room_env: Dict[str, Dict[str, float]] = {}

    def init_rooms(self, room_names: list):
        """
        Set default environmental values for all rooms.
        """
        for room in room_names:
            self.room_env[room] = {
                "temperature": self.base_temp,
                "humidity": self.base_humidity,
                "noise": 30.0  # default base noise level
            }

    def apply_device_effects(self, device_states: Dict[str, dict]):
        """
        Apply effects of all active devices to the corresponding room environments.
        """
        for device_id, state in device_states.items():
            status = state.get("status", "off")

            if status not in ["on", "open"]:
                continue

            if "air_conditioner" in device_id:
                room = self._extract_room(device_id, "air_conditioner")
                self._adjust(room, "temperature", -1.5)

            elif "ventilation_fan" in device_id:
                room = self._extract_room(device_id, "ventilation_fan")
                self._adjust(room, "humidity", -4.0)

            elif "audio_system" in device_id or device_id.startswith("tv_"):
                room = self._extract_room(device_id)
                self._adjust(room, "noise", +15.0)

            elif "window" in device_id or device_id.startswith("blinds_"):
                room = self._extract_room(device_id)
                self._adjust(room, "temperature", +0.5)
                self._adjust(room, "noise", +5.0)

            elif "robot_vacuum" in device_id:
                # Robot makes low-level noise in all rooms while active
                for room in self.room_env:
                    self._adjust(room, "noise", +5.0)

    def _adjust(self, room: str, metric: str, delta: float):
        if room in self.room_env:
            self.room_env[room][metric] += delta

    def get_environment(self, room: str) -> Optional[Dict[str, float]]:
        return self.room_env.get(room)

    def _extract_room(self, device_id: str, prefix: Optional[str] = None) -> str:
        """
        Extract the room name from device_id using known conventions.
        Example: "air_conditioner_kitchen" → "Kitchen"
        """
        raw = device_id
        if prefix and device_id.startswith(prefix + "_"):
            raw = device_id[len(prefix)+1:]
        elif "_" in device_id:
            raw = device_id.split("_", 1)[1]

        # Normalize to match room name casing (e.g., 'kitchen' → 'Kitchen')
        return self._match_room_name(raw)

    def _match_room_name(self, suffix: str) -> str:
        for room in self.room_env:
            if room.lower().endswith(suffix.lower()):
                return room
        return suffix  # fallback if no match
