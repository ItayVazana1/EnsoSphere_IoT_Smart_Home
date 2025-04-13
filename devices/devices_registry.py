"""
Module: devices/devices_registry.py
Purpose: Registers and initializes all smart devices in the system.
Author: Itay Vazana
"""

import json
import os

from devices.tv import TV
from devices.light import Light
from devices.audio_system import AudioSystem
from devices.air_conditioner import AirConditioner
from devices.blinds import Blinds
from devices.door_lock import DoorLock
from devices.pet_door import PetDoor
from devices.pet_feeder import PetFeeder
from devices.vacuum import RobotVacuum
from devices.security import SecuritySystem
from devices.window import SmartWindow
from devices.ventilation_fan import VentilationFan
from devices.pet_door import PetDoor


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "device_room_map.json")

DEVICE_TYPE_MAP = {
    "tv": TV,
    "lights": Light,
    "audio_system": AudioSystem,
    "air_conditioner": AirConditioner,
    "blinds": Blinds,
    "door_lock": DoorLock,
    "pet_door": PetDoor,
    "pet_feeder": PetFeeder,
    "robot_vacuum": RobotVacuum,
    "security_system": SecuritySystem,
    "window": SmartWindow,
    "ventilation_fan": VentilationFan
}

def get_all_devices() -> dict:
    """
    Reads the config file and initializes all device objects.

    Returns:
        dict: Mapping from device_id to Device object.
    """
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        room_map = json.load(f)

    devices = {}
    for devices_in_room in room_map.values():
        for device in devices_in_room:
            device_id = device["id"]
            device_type = device["type"]
            cls = DEVICE_TYPE_MAP.get(device_type)
            if cls:
                devices[device_id] = cls(device_id)

    return devices


if __name__ == "__main__":
    devices = get_all_devices()
    print(f"Total devices registered: {len(devices)}")
    count = 1
    for device_id, device in devices.items():
        print(f"{count}. {device_id} → {device.__class__.__name__}")
        count += 1
