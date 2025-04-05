"""
Test: test_state_schema.py
Purpose: Validate simulator's state_json format against JSON Schema
Author: Itay Vazana
"""

import json
import pytest
from jsonschema import validate, ValidationError
from pathlib import Path

# Import the function under test (when implemented)
# from simulator.simulator_main import generate_state_json

# Load schema once
SCHEMA_PATH = Path("../docs/state_json_schema.json")
with open(SCHEMA_PATH) as f:
    STATE_SCHEMA = json.load(f)

# Dummy valid state_json example (replace with actual function call later)
def dummy_state_json():
    return {
        "timestamp": "2025-08-01T07:30:00",
        "simulation_time": "2025-08-01 07:30",
        "season": "Summer",
        "is_daytime": True,
        "temperature": 31.5,
        "weather": "Sunny",
        "occupants": [{"name": "David", "location": "Living Room"}],
        "rooms": [{"name": "Living Room", "occupants": ["David"]}],
        "house_status": {
            "is_empty": False,
            "active_rooms": ["Living Room"]
        },
        "notes": {"source": "simulator"}
    }

def test_state_json_schema_valid():
    state_json = dummy_state_json()
    try:
        validate(instance=state_json, schema=STATE_SCHEMA)
        print("✔ state_json is valid!")
    except ValidationError as e:
        pytest.fail(f"state_json failed schema validation: {e.message}")
