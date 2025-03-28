

class BaseSensor:
    """
    Base class for all sensors in the Smart Apartment IoT system.

    Attributes:
        sensor_id (str): Unique identifier for the sensor.
        room (str): The room where the sensor is located.
        last_value (any): The most recent value read by the sensor.
    """

    def __init__(self, sensor_id: str, room: str):
        """Initialize the base sensor with its ID and room location."""
        self.sensor_id = sensor_id
        self.room = room
        self.last_value = None

    def read_value(self):
        """
        Read the current value from the environment.

        This method should be implemented by subclasses to provide sensor-specific logic.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_data(self):
        """Return the latest sensor data."""
        return {"sensor_id": self.sensor_id, "room": self.room, "value": self.last_value}