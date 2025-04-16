"""
Module: devices/devices_registry.py
Purpose: Registers and initializes all smart devices in the system from config.
Author: Itay Vazana

This module loads all devices listed in the device_room_map.json config file,
creates matching class instances based on device type, and returns a unified
mapping of device_id → Device instance.
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

# Path to config JSON
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "device_room_map.json")

# Map between device "type" (from config) and Python class
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
    Loads all devices from device_room_map.json and creates class instances.

    Returns:
        dict: { device_id (str) → Device instance }
    """
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        room_map = json.load(f)

    devices = {}
    for room, devices_in_room in room_map.items():
        for device in devices_in_room:
            device_id = device["id"]
            device_type = device["type"]
            cls = DEVICE_TYPE_MAP.get(device_type)
            if cls:
                devices[device_id] = cls(device_id)
            else:
                print(f"[Devices Registry] ⚠️ Unsupported device type: '{device_type}' for ID '{device_id}' (room: {room})")

    return devices


if __name__ == "__main__":
    devices = get_all_devices()
    print(f"✅ Total devices registered: {len(devices)}")
    for i, (device_id, device) in enumerate(devices.items(), 1):
        print(f"{i}. {device_id} → {device.__class__.__name__}")
