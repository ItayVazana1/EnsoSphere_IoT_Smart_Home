from sensors.base_sensor import BaseSensor
import random

class NoiseSensor(BaseSensor):
    """
    Noise Sensor class for Smart Apartment IoT system.

    Simulates measurement of noise levels in decibels.

    Attributes:
        sensor_id (str): Unique identifier for the sensor.
        room (str): Room where the sensor is located.
        last_value (float): Last recorded noise level (in dB).
    """

    def __init__(self, sensor_id: str, room: str, mqtt_client=None, env_manager=None):
        """
        Initialize the noise sensor with optional MQTT and EnvironmentManager.

        Args:
            sensor_id (str): Unique ID for the sensor.
            room (str): Room location.
            mqtt_client (mqtt.Client, optional): MQTT client for publishing.
            env_manager (EnvironmentManager, optional): Simulated time and environment manager.
        """
        super().__init__(sensor_id, room, mqtt_client=mqtt_client, env_manager=env_manager)
        self.last_value = 0.0

    def read_value(self):
        """
        Simulate a random noise level.

        Uses day/night cycle to determine noise range:
        - Daytime: Higher typical noise
        - Nighttime: Quieter

        Returns:
            float: Simulated noise level in decibels.
        """
        if self.env_manager and self.env_manager.is_daytime():
            self.last_value = round(random.uniform(45.0, 80.0), 1)
        else:
            self.last_value = round(random.uniform(30.0, 50.0), 1)
        return self.last_value

    def get_data(self):
        """
        Get the latest noise level data.

        Returns:
            dict: Sensor ID, room, and last recorded noise level.
        """
        return {
            "sensor_id": self.sensor_id,
            "room": self.room,
            "value": self.last_value
        }
