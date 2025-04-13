"""
Module: sensors/sensors_registry.py
Purpose: Registers all sensors in the system for CoreLogic and Simulator use.
Author: Itay Vazana
"""

import os
import json

from sensors.motion_sensor import MotionSensor
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.gas_sensor import GasSensor
from sensors.noise_sensor import NoiseSensor
from sensors.logical_sensor import NoMotionAllRoomsSensor

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "sensor_room_map.json")

SENSOR_TYPE_MAP = {
    "motion": MotionSensor,
    "temperature": TemperatureSensor,
    "humidity": HumiditySensor,
    "gas": GasSensor,
    "noise": NoiseSensor,
    "logical": NoMotionAllRoomsSensor
}


def get_sensors_by_room() -> dict:
    """
    Reads the sensor config and returns a mapping:
    room_name → list of Sensor objects

    Returns:
        dict[str, list[Sensor]]
    """
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        room_map = json.load(f)

    room_sensors = {}
    monitored_rooms = []

    for room, sensors_in_room in room_map.items():
        if room not in ["Entrance", "Global"]:
            monitored_rooms.append(room)

        for sensor in sensors_in_room:
            sensor_id = sensor["id"]
            sensor_type = sensor["type"]
            cls = SENSOR_TYPE_MAP.get(sensor_type)

            if not cls:
                print(f"⚠️ Unknown sensor type: {sensor_type} ({sensor_id})")
                continue

            # Logical sensors are not room-specific
            if sensor_type == "logical":
                continue  # handled separately if needed

            sensor_obj = cls(sensor_id, room)
            room_sensors.setdefault(room, []).append(sensor_obj)

    return room_sensors


def get_logical_sensors() -> list:
    """
    Returns logical sensors (global context sensors)

    Returns:
        list of Sensor objects (logical only)
    """
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        room_map = json.load(f)

    monitored_rooms = [
        room for room in room_map.keys()
        if room not in ["Entrance", "Global"]
    ]

    return [NoMotionAllRoomsSensor("no_motion_all_rooms", monitored_rooms)]


# Legacy alias for compatibility (used in StateBuilder)
def load_all_sensors() -> list:
    room_sensor_map = get_sensors_by_room()
    logical_sensors = get_logical_sensors()
    all_sensors = []

    for sensors in room_sensor_map.values():
        all_sensors.extend(sensors)

    all_sensors.extend(logical_sensors)
    return all_sensors


if __name__ == "__main__":
    all_sensors = load_all_sensors()
    print(f"Total sensors registered: {len(all_sensors)}")
    for i, sensor in enumerate(all_sensors, start=1):
        print(f"{i}. {sensor.sensor_id} → {sensor.__class__.__name__}")
