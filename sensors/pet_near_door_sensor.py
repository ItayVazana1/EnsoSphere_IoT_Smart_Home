import time
import random
from base_sensor import BaseSensor
from core.mqtt_client import create_mqtt_client


class PetNearDoorSensor(BaseSensor):
    """
    Simulates a proximity sensor that detects if the pet is near the door.
    Publishes True (near) or False (away) at regular intervals.
    """

    def __init__(self, sensor_id: str = "pet_near_door", room: str = "entrance", mqtt_client=None, publish_interval: int = 30):
        super().__init__(sensor_id=sensor_id, room=room, mqtt_client=mqtt_client)
        self.publish_interval = publish_interval
        self.presence = False

    def read_value(self) -> bool:
        """
        Simulates pet presence near the door.
        Returns:
            bool: True if the pet is near the door, False otherwise.
        """
        self.presence = random.choices([True, False], weights=[10, 90])[0]
        return self.presence

    def run(self):
        """
        Periodically read and publish sensor value.
        """
        while True:
            self.publish_value()
            time.sleep(self.publish_interval)


if __name__ == "__main__":
    mqtt = create_mqtt_client()
    sensor = PetNearDoorSensor(mqtt_client=mqtt)
    mqtt.loop_start()
    sensor.run()
