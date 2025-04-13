"""
Module: simulator/room.py
Purpose: Defines a Room object that manages its own environmental state and sensor behavior.
Author: Itay Vazana
"""

from typing import List, Dict
from sensors.sensor import Sensor


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

        # Internal environmental state
        self.temperature = 25.0
        self.humidity = 50.0
        self.noise = 30.0

        # Behavior settings
        self.thermal_inertia = 0.4
        self.outside_exposure = 0.2

        # Device-based effects
        self.window_open = False
        self.ac_on = False
        self.devices_active = []

    def apply_device_effect(self, device_id: str):
        self.devices_active.append(device_id)

        if "air_conditioner" in device_id:
            self.ac_on = True
        elif "window" in device_id or device_id.startswith("blinds_"):
            self.window_open = True
        elif "ventilation_fan" in device_id:
            self.humidity -= 4.0
        # noise handled dynamically in update_noise()

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
        self.noise = min(noise, 120.0)  # Cap to prevent nonphysical spikes

    def update_environment(self, outside_temp: float):
        """
        Update room environment based on external temperature and internal device effects.
        Includes noise recalculation and humidity recovery.
        """
        delta = 0.0

        if self.window_open:
            delta += (outside_temp - self.temperature) * 0.5
        else:
            delta += (outside_temp - self.temperature) * self.outside_exposure

        if self.ac_on:
            delta += (22.0 - self.temperature) * 0.4

        self.temperature += delta * (1.0 - self.thermal_inertia)
        self.temperature = round(self.temperature, 1)

        self.update_noise()

        # 💧 Humidity rebalancing (towards 50%) if no fan is active
        if not any("ventilation_fan" in d for d in self.devices_active):
            self.humidity += (50.0 - self.humidity) * 0.1
            self.humidity = round(self.humidity, 1)

        self.reset_state()

    def reset_state(self):
        """
        Clear all transient device flags (called after each tick).
        """
        self.ac_on = False
        self.window_open = False
        self.devices_active.clear()

    def get_environment(self) -> Dict[str, float]:
        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "noise": self.noise
        }

    def has_sensor(self, sensor_id: str) -> bool:
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
