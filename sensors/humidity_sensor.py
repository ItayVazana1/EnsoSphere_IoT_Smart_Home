from sensors.base_sensor import BaseSensor
from core.environment_manager import EnvironmentManager
import random

class HumiditySensor(BaseSensor):
    """
    Humidity Sensor class for Smart Apartment IoT system.

    Simulates humidity reading based on current environment.

    Attributes:
        sensor_id (str): Unique identifier for the sensor.
        room (str): Room where the sensor is located.
        environment (EnvironmentManager): Reference for seasonal humidity behavior.
    """

    def __init__(self, sensor_id: str, room: str, environment: EnvironmentManager):
        """Initialize humidity sensor with environment reference."""
        super().__init__(sensor_id, room)
        self.environment = environment

    def read_value(self):
        """
        Simulate humidity value based on the current season.

        Returns:
            float: Simulated humidity percentage (0.0 to 100.0).
        """
        season = self.environment.current_season
        ranges = {
            'Winter': (40, 70),
            'Spring': (30, 60),
            'Summer': (20, 50),
            'Autumn': (30, 60)
        }
        low, high = ranges[season]
        self.last_value = round(random.uniform(low, high), 1)
        return self.last_value

    def get_data(self):
        """
        Get the latest humidity data.

        Returns:
            dict: Sensor ID, room, and last humidity reading.
        """
        return {
            "sensor_id": self.sensor_id,
            "room": self.room,
            "value": self.last_value
        }
