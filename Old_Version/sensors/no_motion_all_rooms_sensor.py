import time
from base_sensor import BaseSensor
from core.mqtt_client import create_mqtt_client


class NoMotionAllRoomsSensor(BaseSensor):
    """
    Virtual sensor that detects when all motion sensors report 'no_motion'.
    """

    def __init__(self, sensor_id="no_motion_all_rooms", room="virtual", mqtt_client=None, publish_interval=60, motion_sources=None):
        super().__init__(sensor_id=sensor_id, room=room, mqtt_client=mqtt_client)
        self.publish_interval = publish_interval
        self.motion_sources = motion_sources or {}

    def update_motion_sources(self, motion_data: dict):
        """
        Update the current states of motion sensors.
        Example format: { "motion_kitchen": "no_motion", "motion_bedroom": "motion" }
        """
        self.motion_sources = motion_data

    def read_value(self) -> bool:
        """
        Returns True if all rooms report 'no_motion', False otherwise.
        """
        return all(state == "no_motion" for state in self.motion_sources.values())

    def run(self):
        """
        Periodically evaluate motion data and publish result.
        """
        while True:
            self.publish_value()
            time.sleep(self.publish_interval)


if __name__ == "__main__":
    mqtt = create_mqtt_client()
    sensor = NoMotionAllRoomsSensor(mqtt_client=mqtt)

    # Example simulation (this would come from logic elsewhere in a real system)
    test_motion_data = {
        "motion_kitchen": "no_motion",
        "motion_living_room": "no_motion",
        "motion_bedroom": "no_motion"
    }

    sensor.update_motion_sources(test_motion_data)

    mqtt.loop_start()
    sensor.run()
