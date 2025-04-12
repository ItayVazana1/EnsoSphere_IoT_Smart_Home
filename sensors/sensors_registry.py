"""
Module: sensors/sensors_registry.py
Purpose: Registers all sensors in the system for CoreLogic use.
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

CONFIG_PATH = "../config/sensor_room_map.json"

SENSOR_TYPE_MAP = {
    "motion": MotionSensor,
    "temperature": TemperatureSensor,
    "humidity": HumiditySensor,
    "gas": GasSensor,
    "noise": NoiseSensor,
    "logical": NoMotionAllRoomsSensor
}

def get_all_sensors() -> list:
    """
    Reads the sensor config and returns a list of sensor objects.

    Returns:
        list: All initialized sensors.
    """
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        room_map = json.load(f)

    sensors = []
    monitored_rooms = []

    for room, sensors_in_room in room_map.items():
        if room not in ["Entrance", "Global"]:
            monitored_rooms.append(room)

        for sensor in sensors_in_room:
            sensor_id = sensor["id"]
            sensor_type = sensor["type"]
            cls = SENSOR_TYPE_MAP.get(sensor_type)
            if cls:
                if sensor_type == "logical" and sensor_id == "no_motion_all_rooms":
                    sensors.append(cls(sensor_id, monitored_rooms))
                elif sensor_type in ["motion", "noise"]:
                    sensors.append(cls(sensor_id, room))
                else:
                    sensors.append(cls(sensor_id))

    return sensors


if __name__ == "__main__":
    sensors = get_all_sensors()
    print(f"Total sensors registered: {len(sensors)}")
    count = 1
    for sensor in sensors:
        print(f"{count}. {sensor.sensor_id} → {sensor.__class__.__name__}")
        count += 1
