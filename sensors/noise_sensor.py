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

    def __init__(self, sensor_id: str, room: str):
        """Initialize the noise sensor with undefined noise level."""
        super().__init__(sensor_id, room)
        self.last_value = 0.0

    def read_value(self):
        """
        Simulate a random noise level.

        Returns:
            float: Simulated noise level in decibels (30.0 to 90.0).
        """
        self.last_value = round(random.uniform(30.0, 90.0), 1)
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
