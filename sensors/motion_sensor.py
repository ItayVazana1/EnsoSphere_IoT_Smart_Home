from sensors.base_sensor import BaseSensor
import random

class MotionSensor(BaseSensor):
    """
    Motion Sensor class for Smart Apartment IoT system.

    Simulates detection of motion in a room.

    Attributes:
        sensor_id (str): Unique identifier for the sensor.
        room (str): Room where the sensor is located.
        last_value (str): Last motion detection state ("detected"/"none").
    """

    def __init__(self, sensor_id: str, room: str):
        """Initialize motion sensor with no detection."""
        super().__init__(sensor_id, room)
        self.last_value = "none"

    def read_value(self):
        """
        Simulate motion detection.

        Returns:
            str: Either 'detected' or 'none'
        """
        self.last_value = random.choice(["detected", "none"])
        return self.last_value

    def get_data(self):
        """
        Get the latest motion data.

        Returns:
            dict: Sensor ID, room, and last motion state.
        """
        return {
            "sensor_id": self.sensor_id,
            "room": self.room,
            "value": self.last_value
        }
