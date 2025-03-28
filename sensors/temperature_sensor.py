from sensors.base_sensor import BaseSensor
from core.environment_manager import EnvironmentManager

class TemperatureSensor(BaseSensor):
    """
    Temperature Sensor class for Smart Apartment IoT system.

    Reads temperature value from the environment manager.

    Attributes:
        sensor_id (str): Unique identifier for the sensor.
        room (str): Room where the sensor is located.
        environment (EnvironmentManager): Provides current temperature data.
    """

    def __init__(self, sensor_id: str, room: str, environment: EnvironmentManager):
        """Initialize temperature sensor with environment reference."""
        super().__init__(sensor_id, room)
        self.environment = environment

    def read_value(self):
        """
        Reads current temperature from environment.

        Returns:
            float: The current temperature in Celsius.
        """
        env_data = self.environment.get_environment_data()
        self.last_value = env_data["temperature"]
        return self.last_value

    def get_data(self):
        """
        Get the latest temperature data.

        Returns:
            dict: Sensor ID, room, and last temperature value.
        """
        return {
            "sensor_id": self.sensor_id,
            "room": self.room,
            "value": self.last_value
        }
