from sensors.base_sensor import BaseSensor

class WeatherSensor(BaseSensor):
    """
    Weather Sensor for Smart Apartment IoT system.
    Reports weather based on EnvironmentManager simulation.

    Attributes:
        sensor_id (str): Unique identifier.
        room (str): Room where the sensor is located.
    """

    def __init__(self, sensor_id: str, room: str, mqtt_client=None, env_manager=None):
        """
        Initialize weather sensor.
        Uses EnvironmentManager to get current weather conditions.
        """
        super().__init__(sensor_id, room, mqtt_client=mqtt_client, env_manager=env_manager)
        self.last_value = None

    def read_value(self):
        """
        Reads the current weather condition from EnvironmentManager.

        Returns:
            str: Simulated weather condition (e.g., "Clear", "Rainy").
        """
        if self.env_manager:
            self.last_value = self.env_manager.current_weather
        else:
            self.last_value = "Unknown"
        return self.last_value

    def get_data(self):
        """
        Get current weather data.

        Returns:
            dict: Includes sensor ID, room, and condition.
        """
        return {
            "sensor_id": self.sensor_id,
            "room": self.room,
            "value": self.last_value
        }
