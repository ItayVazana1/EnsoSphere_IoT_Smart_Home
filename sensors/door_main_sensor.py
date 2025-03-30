import time
import random
from base_sensor import BaseSensor
from core.mqtt_client import create_mqtt_client


class DoorMainSensor(BaseSensor):
    """
    Simulates a door sensor for the main entrance.
    Publishes 'opened' or 'closed' states at regular intervals.
    """

    def __init__(self, sensor_id: str = "door_main", room: str = "entrance", mqtt_client=None, publish_interval: int = 30):
        super().__init__(sensor_id=sensor_id, room=room, mqtt_client=mqtt_client)
        self.publish_interval = publish_interval
        self.state = "closed"

    def read_value(self) -> str:
        """
        Simulates a door opening/closing randomly.
        Returns:
            str: "opened" or "closed"
        """
        self.state = random.choices(["closed", "opened"], weights=[85, 15])[0]
        return self.state

    def run(self):
        """
        Periodically read and publish sensor value.
        """
        while True:
            self.publish_value()
            time.sleep(self.publish_interval)


if __name__ == "__main__":
    mqtt = create_mqtt_client()
    sensor = DoorMainSensor(mqtt_client=mqtt)
    mqtt.loop_start()
    sensor.run()
