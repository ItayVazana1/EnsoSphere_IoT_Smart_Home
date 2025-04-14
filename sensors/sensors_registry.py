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


def get_sensors_by_room(shared_publisher=None) -> dict:
    """
    Reads the sensor config and returns a mapping:
    room_name → list of Sensor objects

    Args:
        shared_publisher (SensorPublisher, optional): Shared instance to inject into sensors

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

            if sensor_type == "logical":
                continue  # Logical sensors handled separately

            sensor_obj = cls(sensor_id, room, publisher=shared_publisher)
            room_sensors.setdefault(room, []).append(sensor_obj)

    return room_sensors


def get_logical_sensors(shared_publisher=None) -> list:
    """
    Returns logical sensors (global context sensors)

    Args:
        shared_publisher (SensorPublisher, optional): Shared instance to inject into logical sensors

    Returns:
        list of Sensor objects (logical only)
    """
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        room_map = json.load(f)

    monitored_rooms = [
        room for room in room_map.keys()
        if room not in ["Entrance", "Global"]
    ]

    return [NoMotionAllRoomsSensor("no_motion_all_rooms", monitored_rooms, publisher=shared_publisher)]


def load_all_sensors(shared_publisher=None) -> list:
    """
    Loads all sensors (room + logical) with optional shared publisher.

    Args:
        shared_publisher (SensorPublisher, optional): MQTT publisher instance

    Returns:
        list[Sensor]: List of all sensor objects
    """
    room_sensor_map = get_sensors_by_room(shared_publisher)
    logical_sensors = get_logical_sensors(shared_publisher)
    all_sensors = []

    for sensors in room_sensor_map.values():
        all_sensors.extend(sensors)

    all_sensors.extend(logical_sensors)
    return all_sensors
