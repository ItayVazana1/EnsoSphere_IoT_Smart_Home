"""
Test: test_state_builder.py
Purpose: Validate state_json output from StateBuilder matches official JSON schema
Author: Itay Vazana
"""

import json
import pytest
from jsonschema import validate, ValidationError
from datetime import datetime

from simulator.time_manager import TimeManager
from simulator.weather_engine import WeatherEngine
from simulator.occupant_engine import OccupantEngine
from simulator.state_builder import StateBuilder

SCHEMA_DIR = "../docs/state_json_schema.json"
ROUTINES_DIR = "../routines/"
def test_state_builder_matches_schema():
    # Load schema
    with open(SCHEMA_DIR) as f:
        schema = json.load(f)

    # Initialize engines
    tm = TimeManager(start_datetime=datetime(2025, 8, 1, 6, 0))
    we = WeatherEngine()
    oe = OccupantEngine(season="Summer", routines_dir=ROUTINES_DIR)
    sb = StateBuilder(tm, we, oe)

    # Generate one state
    state = sb.build_state(["Testy"])

    # Validate each field manually for clearer output
    for key in schema["required"]:
        assert key in state, f"Missing required field: {key}"
        print(f"✔ Field '{key}' exists.")

    # Validate full schema with jsonschema
    try:
        validate(instance=state, schema=schema)
        print("✔ Full state_json matches schema.")
    except ValidationError as e:
        print(f"❌ Schema validation failed: {e.message}")
        pytest.fail("state_json did not match schema")


    # ✅ Pretty-print final output
    print("\n📦 Final state_json output:\n" + json.dumps(state, indent=2))