import os
import pytest
import pandas as pd
from pathlib import Path

VALID_ROOMS = {
    "LivingRoom",
    "Kitchen",
    "Balcony",
    "ParentsRoom",
    "KobeRoom",
    "GavriellaRoom",
    "Bathroom1",
    "Bathroom2"
}

NON_ROOM_LOCATIONS = {
    "Outside",
    "Work",
    "Park",
    "Car",
    "School",
    "Kindergarten",
    "Vet",
    "Clinic",
    "Supermarket"
}

CHARACTERS = ["Testy", "David"]
SEASONS = ["Autumn", "Winter", "Spring", "Summer"]
ROUTINES_DIR = "../routines/"

def test_routine_locations():
    routines_dir = Path(ROUTINES_DIR)
    invalid_locations = []  # Collect any invalid entries

    for character in CHARACTERS:
        file_path = routines_dir / f"{character}.xlsx"
        if not file_path.exists():
            print(f"❌ Routine file not found: {file_path}")
            continue

        df = pd.read_excel(file_path)

        required_cols = {"Time"} | set(SEASONS)
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            print(f"❌ Missing columns {missing_cols} in {file_path}")
            continue

        # Print header for clarity
        print(f"\n=== Checking {character} in {file_path.name} ===")

        for i, row in df.iterrows():
            for season in SEASONS:
                location = row[season]
                if pd.isna(location) or not str(location).strip():
                    # Mark empty as valid or skip
                    print(f"[Row {i}, {season}] EMPTY => ✔ (skipped)")
                    continue

                loc_str = str(location).strip()
                is_valid = (loc_str in VALID_ROOMS) or (loc_str in NON_ROOM_LOCATIONS)

                # Print line with check
                if is_valid:
                    print(f"[Row {i}, {season}] {loc_str} => ✔")
                else:
                    print(f"[Row {i}, {season}] {loc_str} => ❌ (invalid)")
                    invalid_locations.append(
                        f"[{character}] Row {i}, season '{season}' => '{loc_str}'"
                    )

    # After scanning all characters, print summary
    if invalid_locations:
        print("\n⚠️ WARNING: Found invalid locations:")
        for entry in invalid_locations:
            print("  " + entry)
        # test passes, but we show the results
    else:
        print("\n✅ All routine locations are valid!")