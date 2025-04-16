"""
Module: simulator/device_state_fetcher.py
Purpose: Fetch latest known device states from MySQL to be used in environmental simulation.
Author: Itay Vazana
"""

import mysql.connector
import json
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "ensosphere")
}

def fetch_device_states() -> Dict[str, dict]:
    """
    Fetch the latest state of all devices from the device_states table.

    Returns:
        dict: {device_id: state_dict, ...}
    """
    device_states = {}

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT device_id, state_json FROM device_states")

        for device_id, state_json in cursor.fetchall():
            try:
                state = json.loads(state_json)
                device_states[device_id] = state
            except json.JSONDecodeError:
                print(f"⚠️ Could not parse state for device: {device_id}")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ MySQL error in fetch_device_states: {err}")

    return device_states

def fetch_device_states_by_room(device_room_map_path="config/device_room_map.json") -> Dict[str, Dict[str, dict]]:
    """
    Fetches device states and organizes them per room using device-room mapping.

    Args:
        device_room_map_path (str): Path to the device-room mapping JSON file.

    Returns:
        Dict[str, Dict[str, dict]]: {room_name: {device_id: state_dict}}
    """
    try:
        with open(device_room_map_path, "r") as f:
            room_map = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load device-room map: {e}")
        return {}

    all_states = fetch_device_states()
    room_states: Dict[str, Dict[str, dict]] = {}

    for room_name, devices in room_map.items():
        room_states[room_name] = {}
        for device in devices:
            device_id = device["id"]
            if device_id in all_states:
                room_states[room_name][device_id] = all_states[device_id]

    return room_states

def fetch_device_metadata_by_room(
    device_room_map_path="config/device_room_map.json",
    metadata_path="config/device_metadata.json"
) -> Dict[str, Dict[str, dict]]:
    """
    Combines live device states from DB with device metadata, organized by room.

    Returns:
        Dict[str, Dict[str, dict]]: {
            room_name: {
                device_id: {
                    "type": str,
                    "state": dict,
                    "effects": dict
                }
            }
        }
    """
    try:
        with open(device_room_map_path, "r") as f:
            room_map = json.load(f)
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load metadata or map: {e}")
        return {}

    all_states = fetch_device_states()
    enriched: Dict[str, Dict[str, dict]] = {}

    for room_name, devices in room_map.items():
        enriched[room_name] = {}
        for device in devices:
            device_id = device["id"]
            device_type = device["type"]
            state = all_states.get(device_id, {})
            type_info = metadata.get(device_type, {})
            enriched[room_name][device_id] = {
                "type": device_type,
                "state": state,
                "effects": type_info.get("environment_effects", {})
            }

    return enriched

if __name__ == "__main__":
    states = fetch_device_metadata_by_room()
    print(f"Total rooms with metadata: {len(states)}")
    for room, devices in states.items():
        print(f"\n📍 {room}:")
        for dev, info in devices.items():
            print(f"  {dev} ({info['type']}) → {info['state']} | Effects: {info['effects']}")