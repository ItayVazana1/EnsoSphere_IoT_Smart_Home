"""
Module: simulator/state_builder.py
Purpose: Assemble full state_json using time, weather, occupants, and sensor values, including room environmental effects.
Author: Itay Vazana
"""

from datetime import datetime
from typing import List, Dict

from simulator.core.world import World
from simulator.core.house import House
from sensors.sensors_registry import load_all_sensors


class StateBuilder:
    def __init__(self, world: World, house: House):
        self.world = world
        self.house = house
        self.sensors = load_all_sensors()
        self.expected_sensor_ids = self._extract_sensor_ids()

    def _extract_sensor_ids(self) -> List[str]:
        """
        Builds a flat list of all expected sensor IDs from loaded sensors.
        """
        return [sensor.get_id() for sensor in self.sensors]

    def build_state(self, character_names: List[str], device_states: Dict[str, dict]) -> Dict:
        # Extract world state
        current_datetime: datetime = self.world.get_datetime()
        time_str = self.world.get_time_str()
        season = self.world.get_season()
        is_daytime = self.world.is_daytime()
        weather = self.world.get_weather()
        outdoor_temp = self.world.get_outside_temperature()

        # Update house based on world + characters + devices
        self.house.update_occupants_by_time(character_names, time_str, season)
        self.house.update_devices(device_states)
        self.house.update_environment(outdoor_temp)

        # Extract from house
        occupants = self.house.get_occupants()
        rooms = self.house.get_room_map()
        is_empty = len(occupants) == 0
        active_rooms = self.house.get_active_rooms()
        room_state = self.house.get_room_states()
        house_summary = self.house.get_summary()

        # Base state_json
        state = {
            "timestamp": current_datetime.isoformat(),
            "simulation_time": current_datetime.strftime("%Y-%m-%d %H:%M"),
            "season": season,
            "is_daytime": is_daytime,
            "temperature": outdoor_temp,
            "weather": weather,
            "occupants": occupants,
            "rooms": rooms,
            "house_status": {
                "is_empty": is_empty,
                "active_rooms": active_rooms,
                "room_state": room_state,
                "summary": house_summary
            },
            "notes": {
                "source": "simulator"
            }
        }

        # Sensor outputs from rooms
        sensor_outputs = self.house.generate_sensor_outputs(state)

        # Evaluate logical/custom sensors
        sensor_lookup = {s.get_id(): s for s in self.sensors}
        for sensor_id in self.expected_sensor_ids:
            if sensor_id not in sensor_outputs:
                sensor = sensor_lookup.get(sensor_id)
                if sensor:
                    try:
                        sensor_outputs[sensor_id] = sensor.evaluate_and_store(state, self.house)
                    except Exception as e:
                        print(f"⚠️ Sensor {sensor_id} evaluation failed: {e}")
                        sensor_outputs[sensor_id] = None
                else:
                    print(f"⚠️ Sensor {sensor_id} not implemented. Setting value to None.")
                    sensor_outputs[sensor_id] = None

        state["sensors"] = sensor_outputs
        return state
