from sensors.base_sensor import BaseSensor
import random

class GasSensor(BaseSensor):
    """
    Gas Sensor class for Smart Apartment IoT system.

    Simulates gas concentration level detection.

    Attributes:
        sensor_id (str): Unique identifier for the sensor.
        room (str): Room where the sensor is located.
    """

    def __init__(self, sensor_id: str, room: str, mqtt_client=None, env_manager=None):
        """
        Initialize gas sensor with optional MQTT client and environment manager.

        Args:
            sensor_id (str): Unique sensor ID.
            room (str): Room location.
            mqtt_client (mqtt.Client, optional): MQTT client for publishing.
            env_manager (EnvironmentManager, optional): Simulated environment for timestamp.
        """
        super().__init__(sensor_id, room, mqtt_client=mqtt_client, env_manager=env_manager)

    def read_value(self):
        """
        Simulate gas concentration level.

        Returns:
            float: Simulated gas level in ppm (parts per million).
        """
        self.last_value = round(random.uniform(200, 500), 2)
        return self.last_value
