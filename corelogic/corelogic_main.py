"""
Module: corelogic/corelogic_main.py
Purpose: Simulator debug mode – randomly toggles device states to test simulator sensor response.
Author: Itay Vazana
"""

import time
import json
import random
import os
from corelogic.db_connector import DBConnector

# Optional concise output mode (cleaner logging)
CONCISE_MODE = os.getenv("CORE_LOGIC_CONCISE_MODE", "False").lower() in ("1", "true", "yes")

DEVICE_MAP_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "device_room_map.json")

def load_device_map() -> dict:
    with open(DEVICE_MAP_PATH, "r", encoding="utf-8") as f:
        full_map = json.load(f)
        # Flatten to {device_id: {"type": str, "room": str}}
        flat_map = {}
        for room, devices in full_map.items():
            for device in devices:
                flat_map[device["id"]] = {"type": device["type"], "room": room}
        return flat_map

def parse_device_type(device_type: str) -> str:
    names = {
        "air_conditioner": "Air Conditioner",
        "ventilation_fan": "Ventilation Fan",
        "audio_system": "Audio System",
        "tv": "Television",
        "window": "Window",
        "blinds": "Blinds",
        "robot_vacuum": "Robot Vacuum",
        "lights": "Lights",
        "door_lock": "Main Door Lock",
        "pet_door": "Pet Door",
        "pet_feeder": "Pet Feeder",
        "security_system": "Security System"
    }
    return names.get(device_type, device_type.capitalize())

if __name__ == "__main__":
    print("\n🧪 CoreLogic DEBUG MODE – randomly toggling device states for simulator testing.\n")

    db = DBConnector()
    device_map = load_device_map()

    while True:
        try:
            state = db.get_next_unprocessed_state()

            if state:
                state_id = state['state_id']
                all_device_ids = list(device_map.keys())
                selected_devices = random.sample(all_device_ids, k=min(len(all_device_ids), random.randint(2, 4)))
                actions = []

                for dev_id in selected_devices:
                    new_status = random.choice(["on", "off"])
                    meta = device_map[dev_id]
                    room = meta.get("room", "Unknown")
                    device_type = parse_device_type(meta.get("type", "Unknown"))

                    actions.append({
                        "device_id": dev_id,
                        "command": {"status": new_status}
                    })

                    if not CONCISE_MODE:
                        print(f"⚙️ {device_type} in {room}: {dev_id} → {new_status}")

                db.insert_device_states(actions)
                db.mark_state_as_processed(state_id)

                if CONCISE_MODE:
                    changes_str = ", ".join(f"{a['device_id']} → {a['command']['status']}" for a in actions)
                    print(f"🌀 Tick {state_id} → Devices changed: {changes_str}")
                else:
                    print(f"✔️ Tick {state_id} processed with {len(actions)} device changes.")

            else:
                print("⏳ No new tick found. Waiting...")
                time.sleep(5)

        except Exception as e:
            import traceback
            print(f"\n❌ Error during CoreLogic debug loop: {e}")
            traceback.print_exc()
            time.sleep(5)