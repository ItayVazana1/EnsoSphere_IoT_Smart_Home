"""
Module: simulator/room.py
Purpose: Represents a smart room and applies device effects based on state and metadata.
Author: Itay Vazana
"""

import random
import json
import os
from typing import Dict, List
from sensors.sensor import Sensor

# Load metadata from config
def load_device_metadata():
    config_path = os.path.join("config", "device_metadata.json")
    with open(config_path, "r") as f:
        return json.load(f)

DEVICE_METADATA = load_device_metadata()


class Room:
    def __init__(self, name: str, sensors: List[Sensor]):
        """
        Initialize a Room with base environmental conditions and associated sensors.

        Args:
            name (str): Name of the room (e.g., "Kitchen").
            sensors (List[Sensor]): List of Sensor objects associated with this room.
        """
        self.name = name
        self.sensors = sensors
        self.temperature = 25.0
        self.noise = 30.0
        self.humidity = 50.0
        self.gas = 0.1
        self.device_states: Dict[str, dict] = {}
        self.thermal_inertia = 0.4
        self.outside_exposure = 0.2
        self.devices_active = []

    def update_sensor(self, sensor):
        """Append a new sensor to the room."""
        self.sensors.append(sensor)

    def apply_device_state(self, device_id: str, state: dict):
        """
        Register a device's state for this tick.

        Args:
            device_id (str): ID of the device.
            state (dict): Device state dictionary.
        """
        self.device_states[device_id] = state
        self.devices_active.append(device_id)

    def apply_all_device_effects(self):
        """Apply all device environmental effects for this tick."""
        for device_id, state in self.device_states.items():
            self.apply_device_effect(device_id, state)

    def apply_device_effect(self, device_id: str, state: dict):
        """
        Apply effects of a single device to the room environment.

        Args:
            device_id (str): ID of the device.
            state (dict): Current state of the device.
        """
        device_type = self._extract_device_type(device_id)
        device_info = DEVICE_METADATA.get(device_type)
        if not device_info:
            return

        effects = device_info.get("environment_effects", {})

        for prop, impact in effects.items():
            if isinstance(impact, dict):
                mode_key = state.get("mode") or state.get("status")
                change = impact.get(mode_key)
                if change is not None:
                    self._apply_environment_change(prop, change)
            elif isinstance(impact, (int, float)):
                self._apply_environment_change(prop, impact)

    def _extract_device_type(self, device_id: str) -> str:
        """Heuristic extraction of device type from its ID."""
        if device_id.startswith("tv_"):
            return "tv"
        for known_type in DEVICE_METADATA:
            if known_type in device_id:
                return known_type
        return "unknown"

    def _apply_environment_change(self, property_name: str, delta: float):
        """Applies a delta change to the room's environment."""
        if property_name == "temperature":
            self.temperature += delta
        elif property_name == "noise":
            self.noise += delta
        elif property_name == "humidity":
            self.humidity += delta
        elif property_name == "gas":
            self.gas += delta

    def update_environment(self, outside_temp: float):
        """
        Update room environment based on external temperature and internal device effects.
        Includes noise recalculation and humidity recovery.

        Args:
            outside_temp (float): Current outside temperature.
        """
        delta = 0.0

        has_window = any("window" in d or d.startswith("blinds_") for d in self.devices_active)
        has_ac = any("air_conditioner" in d for d in self.devices_active)
        has_fan = any("ventilation_fan" in d for d in self.devices_active)

        if has_window:
            delta += (outside_temp - self.temperature) * 0.5
        else:
            delta += (outside_temp - self.temperature) * self.outside_exposure

        if has_ac:
            delta += (22.0 - self.temperature) * 0.4

        self.temperature += delta * (1.0 - self.thermal_inertia)
        self.temperature = round(self.temperature, 1)

        self.update_noise()

        if not has_fan:
            self.humidity += (50.0 - self.humidity) * 0.1
            self.humidity = round(self.humidity, 1)

        self.reset_state()

    def update_noise(self):
        """
        Recalculate noise level based on currently active devices.
        Prevents unrealistic accumulation over time.
        """
        base = 30.0
        noise = base
        for device_id in self.devices_active:
            if "audio_system" in device_id or device_id.startswith("tv_"):
                noise += 15.0
            elif "robot_vacuum" in device_id:
                noise += 5.0
        self.noise = min(noise, 120.0)

    def reset_state(self):
        """Clear all transient device state after tick."""
        self.devices_active.clear()

    def get_sensor_values(self) -> Dict[str, float]:
        """Returns the current environmental state of the room."""
        return {
            "temperature": round(self.temperature, 1),
            "noise": round(self.noise, 1),
            "humidity": round(self.humidity, 1),
            "gas": round(self.gas, 2),
        }

    def has_sensor(self, sensor_id: str) -> bool:
        """Checks if a sensor with given ID exists in this room."""
        return any(sensor.sensor_id == sensor_id for sensor in self.sensors)

    def generate_sensor_outputs(self, state_json: dict, house) -> Dict[str, float]:
        """
        Evaluate all local sensors and return their outputs.

        Args:
            state_json (dict): Current tick's simulation state
            house: Reference to full House (for logic sensors if needed)

        Returns:
            Dict[sensor_id, value]
        """
        outputs = {}
        for sensor in self.sensors:
            try:
                outputs[sensor.sensor_id] = sensor.evaluate_and_store(state_json, house)
            except Exception as e:
                print(f"⚠️ Sensor {sensor.sensor_id} evaluation failed in Room {self.name}: {e}")
                outputs[sensor.sensor_id] = None
        return outputs

    def get_environment(self) -> dict:
        """
        Returns the current environmental state of the room.
        Matches structure used by simulator output and sensors.

        Returns:
            dict: { "temperature": float, "noise": float, "humidity": float, "gas": float }
        """
        return self.get_sensor_values()
