from sensors.base_sensor import BaseSensor
import random

class GasSensor(BaseSensor):
    """
    Gas Sensor class for Smart Apartment IoT system.

    Simulates detection of gas concentration levels.

    Attributes:
        sensor_id (str): Unique identifier for the sensor.
        room (str): Room where the sensor is located (usually Kitchen).
        last_value (str): Detected gas level state ('safe', 'warning', 'critical').
    """

    def __init__(self, sensor_id: str, room: str):
        """Initialize the gas sensor with safe state."""
        super().__init__(sensor_id, room)
        self.last_value = "safe"

    def read_value(self):
        """
        Simulate gas detection state.

        Returns:
            str: One of 'safe', 'warning', or 'critical'
        """
        self.last_value = random.choices(
            ["safe", "warning", "critical"],
            weights=[0.85, 0.10, 0.05],  # mostly safe
            k=1
        )[0]
        return self.last_value

    def get_data(self):
        """
        Get the latest gas sensor data.

        Returns:
            dict: Sensor ID, room, and current gas level state.
        """
        return {
            "sensor_id": self.sensor_id,
            "room": self.room,
            "value": self.last_value
        }
