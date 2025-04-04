from sensors.base_sensor import BaseSensor
import random

class TemperatureSensor(BaseSensor):
    """
    Temperature Sensor class for Smart Apartment IoT system.

    Simulates reading temperature in a room using either
    the EnvironmentManager or random fallback.

    Attributes:
        sensor_id (str): Unique identifier for the sensor.
        room (str): Room where the sensor is located.
        last_value (float): Last temperature value.
    """

    def __init__(self, sensor_id: str, room: str, mqtt_client=None, env_manager=None):
        """Initialize temperature sensor with MQTT and optional environment support."""
        super().__init__(sensor_id, room, mqtt_client=mqtt_client, env_manager=env_manager)

    def read_value(self):
        """
        Reads current temperature from EnvironmentManager if available,
        otherwise simulates it.

        Returns:
            float: Temperature in Celsius.
        """
        if self.env_manager:
            self.last_value = self.env_manager.current_temperature()
        else:
            self.last_value = round(random.uniform(18.0, 26.0), 1)
        return self.last_value