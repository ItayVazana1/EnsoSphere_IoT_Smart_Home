import json
from datetime import datetime

class BaseSensor:
    """
    Base class for all sensors in the Smart Apartment IoT system.

    Attributes:
        sensor_id (str): Unique identifier for the sensor.
        room (str): The room where the sensor is located.
        last_value (any): The most recent value read by the sensor.
        mqtt_client (mqtt.Client): MQTT client for publishing sensor data.
        env_manager (EnvironmentManager): Provides simulated time and environment.
    """

    def __init__(self, sensor_id: str, room: str, mqtt_client=None, env_manager=None):
        """Initialize the base sensor with its ID, room location, MQTT client, and EnvironmentManager."""
        self.sensor_id = sensor_id
        self.room = room
        self.last_value = None
        self.mqtt_client = mqtt_client
        self.env_manager = env_manager

    def read_value(self):
        """
        Read the current value from the environment.

        This method should be implemented by subclasses to provide sensor-specific logic.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_data(self):
        """Return the latest sensor data."""
        return {
            "sensor_id": self.sensor_id,
            "room": self.room,
            "value": self.last_value
        }

    def get_mqtt_topic(self):
        """
        Returns the MQTT topic to which this sensor publishes.
        Format: MyHome/<room>/<sensor_type>/<sensor_id>
        """
        sensor_type = self.__class__.__name__.lower()
        return f"MyHome/{self.room}/{sensor_type}/{self.sensor_id}"

    def publish_value(self):
        """
        Reads a new value and publishes it via MQTT if the client exists.
        Uses simulated time from EnvironmentManager if provided.
        """
        self.last_value = self.read_value()
        timestamp = (
            self.env_manager.simulated_time.isoformat()
            if self.env_manager else datetime.now().isoformat()
        )

        if self.mqtt_client:
            topic = self.get_mqtt_topic()
            payload = json.dumps({
                "sensor_id": self.sensor_id,
                "room": self.room,
                "value": self.last_value,
                "timestamp": timestamp
            })
            self.mqtt_client.publish(topic, payload)
            print(f"[MQTT][Sensor] Published to '{topic}': {payload}")
