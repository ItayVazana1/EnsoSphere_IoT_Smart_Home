from sensors.base_sensor import BaseSensor
import random

class HumiditySensor(BaseSensor):
    """
    Humidity Sensor class for Smart Apartment IoT system.

    Simulates humidity reading based on current environment.

    Attributes:
        sensor_id (str): Unique identifier for the sensor.
        room (str): Room where the sensor is located.
        last_value (float): Last humidity value.
    """

    def __init__(self, sensor_id: str, room: str, mqtt_client=None, env_manager=None):
        """Initialize humidity sensor with MQTT and optional environment manager."""
        super().__init__(sensor_id, room, mqtt_client=mqtt_client, env_manager=env_manager)

    def read_value(self):
        """
        Simulate or retrieve humidity value based on the current season.

        Returns:
            float: Simulated humidity percentage (0.0 to 100.0).
        """
        if self.env_manager:
            season = self.env_manager.current_season
            ranges = {
                'Winter': (40, 70),
                'Spring': (30, 60),
                'Summer': (20, 50),
                'Autumn': (30, 60)
            }
            low, high = ranges.get(season, (30, 60))
        else:
            low, high = 30, 60

        self.last_value = round(random.uniform(low, high), 1)
        return self.last_value
