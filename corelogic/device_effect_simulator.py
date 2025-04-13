"""
Module: corelogic/device_effect_simulator.py
Purpose: Simulate the physical environmental effects of active devices (e.g., AC, music, etc.)
Author: Itay Vazana
"""

import json
from typing import Dict
from corelogic.db_connector import DBConnector
import logging
import json
from devices.devices_registry import CONFIG_PATH


# Device effect mapping based on full registered list (32 devices)
device_to_effects = {
    "air_conditioner": {
        "sensor_type": "temperature",
        "effect": lambda x: max(x - 0.4, 16.0)
    },
    "tv": {
        "sensor_type": "noise",
        "effect": lambda x: min(x + 15, 100.0)
    },
    "audio_system": {
        "sensor_type": "noise",
        "effect": lambda x: min(x + 30, 100.0)
    },
    "ventilation_fan": {
        "sensor_type": "humidity",
        "effect": lambda x: max(x - 5, 0.0)
    },
    "robot_vacuum": {
        "sensor_type": "noise",
        "effect": lambda x: min(x + 20, 100.0)
    }
}

class DeviceEffectSimulator:
    def __init__(self, db_connector: DBConnector):
        self.db = db_connector
        self.logger = logging.getLogger(__name__)

    def apply_device_effects(self, state_json: Dict) -> Dict:
        rooms = {room["name"]: room for room in state_json.get("rooms", [])}

        for room_name, devices in self._get_devices_by_room().items():
            for device in devices:
                device_id = device["id"]
                device_type = device["type"]

                if device_type not in device_to_effects:
                    continue

                status = self.db.get_device_current_state(device_id)
                if not status or status.get("status") != "on":
                    continue

                effect_info = device_to_effects[device_type]
                sensor_type = effect_info["sensor_type"]
                sensor_id = f"{sensor_type}_{room_name.lower()}"

                try:
                    current_value = self._extract_sensor_value(state_json, sensor_id)
                    new_value = effect_info["effect"](current_value)
                    self._inject_sensor_value(state_json, sensor_id, new_value)

                    # DEBUG PRINT
                    print(f"📡 [{room_name}] {device_id} ({device_type}) is ON → {sensor_id}: {current_value:.1f} → {new_value:.1f}")
                except Exception as e:
                    self.logger.warning(f"[DeviceEffectSimulator] Could not apply effect for {device_id}: {e}")

        return state_json


    def _get_devices_by_room(self) -> Dict[str, list]:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            DEVICE_ROOM_MAP = json.load(f)
        return DEVICE_ROOM_MAP


    def _extract_sensor_value(self, state_json: Dict, sensor_id: str) -> float:
        for room in state_json.get("rooms", []):
            if sensor_id.endswith(room["name"].lower()):
                return float(room.get(sensor_id, 0))
        if sensor_id in state_json:
            return float(state_json[sensor_id])
        raise KeyError(f"Sensor {sensor_id} not found in state")

    def _inject_sensor_value(self, state_json: Dict, sensor_id: str, new_value: float):
        for room in state_json.get("rooms", []):
            if sensor_id.endswith(room["name"].lower()):
                room[sensor_id] = round(new_value, 2)
                return
        if sensor_id in state_json:
            state_json[sensor_id] = round(new_value, 2)
