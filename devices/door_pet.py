from base_device import BaseDevice
from core.mqtt_client import create_mqtt_client


class DoorPet(BaseDevice):
    """
    Simulates a smart pet door.
    Responds to: lock, unlock, auto_mode.
    """

    def __init__(self, device_id: str = "door_pet", room: str = "entrance", mqtt_client=None):
        super().__init__(device_id=device_id, room=room, mqtt_client=mqtt_client)

    def receive_command(self, command: str, parameters: dict = None):
        """
        Handles incoming MQTT commands to control the pet door.
        """
        if command == "lock":
            self.state = "locked"
        elif command == "unlock":
            self.state = "unlocked"
        elif command == "auto_mode":
            self.state = "auto"
        else:
            print(f"[PET_DOOR] Unknown command received: {command}")
            return

        print(f"[PET_DOOR] Pet door state: {self.state.upper()}")
        self.publish_status()


if __name__ == "__main__":
    mqtt = create_mqtt_client()
    mqtt.loop_start()

    pet_door = DoorPet(mqtt_client=mqtt)
