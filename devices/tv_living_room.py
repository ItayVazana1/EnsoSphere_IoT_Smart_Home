from base_device import BaseDevice
from core.mqtt_client import create_mqtt_client


class TVLivingRoom(BaseDevice):
    """
    Simulates a smart TV in the living room.
    Responds to commands: turn_on, turn_off.
    """

    def __init__(self, device_id: str = "tv_living_room", room: str = "living_room", mqtt_client=None):
        super().__init__(device_id=device_id, room=room, mqtt_client=mqtt_client)

    def receive_command(self, command: str, parameters: dict = None):
        """
        Handles incoming MQTT commands and updates the device state.
        """
        if command == "turn_on":
            self.state = "on"
        elif command == "turn_off":
            self.state = "off"
        else:
            print(f"[TV] Unknown command received: {command}")
            return

        print(f"[TV] Living Room TV turned {self.state.upper()}")
        self.publish_status()


if __name__ == "__main__":
    mqtt = create_mqtt_client()
    mqtt.loop_start()

    tv = TVLivingRoom(mqtt_client=mqtt)
    # No need to call any listen method – subscription handled by BaseDevice
