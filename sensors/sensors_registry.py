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
                # Logical sensor (e.g., no_motion_all_rooms) receives full monitored room list
                if sensor_type == "logical" and sensor_id == "no_motion_all_rooms":
                    sensors.append(cls(sensor_id, monitored_rooms))

                # Room-based sensors (motion, noise, temperature, humidity, gas)
                elif sensor_type in ["motion", "noise", "temperature", "humidity", "gas"]:
                    sensors.append(cls(sensor_id, room))

                # (Other types if added later can go here...)
                else:
                    print(f"⚠️ Unsupported sensor type or missing room binding: {sensor_id}")

    return sensors


# Alias for simulator usage
load_all_sensors = get_all_sensors

if __name__ == "__main__":
    sensors = get_all_sensors()
    print(f"Total sensors registered: {len(sensors)}")
    for i, sensor in enumerate(sensors, start=1):
        print(f"{i}. {sensor.sensor_id} → {sensor.__class__.__name__}")
