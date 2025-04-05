"""
Module: simulator/state_schema.py
Purpose: Define the official state_json schema format for EnsoSphere simulation output
Author: Itay Vazana
"""

STATE_JSON_FIELDS = {
    "timestamp": str,
    "simulation_time": str,
    "season": str,
    "is_daytime": bool,
    "temperature": float,
    "weather": str,
    "occupants": list,
    "rooms": list,
    "house_status": dict,
    "notes": dict
}

def validate_state_json(state_json: dict) -> bool:
    """
    Validates the structure of a state_json object.

    Args:
        state_json (dict): The JSON object to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    for key, expected_type in STATE_JSON_FIELDS.items():
        if key not in state_json:
            print(f"Missing field: {key}")
            return False
        if not isinstance(state_json[key], expected_type):
            print(f"Field '{key}' has wrong type: expected {expected_type}, got {type(state_json[key])}")
            return False
    return True
