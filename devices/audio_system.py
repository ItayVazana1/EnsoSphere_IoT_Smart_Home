from base_device import BaseDevice
from core.mqtt_client import create_mqtt_client


class AudioSystem(BaseDevice):
    """
    Simulates a smart home audio system.
    Responds to: play_music, pause, reduce_volume, turn_off.
    """

    def __init__(self, device_id: str = "audio_system", room: str = "living_room", mqtt_client=None):
        super().__init__(device_id=device_id, room=room, mqtt_client=mqtt_client)

    def receive_command(self, command: str, parameters: dict = None):
        """
        Handles incoming MQTT commands and updates the audio system state.
        """
        if command == "play_music":
            self.state = "playing"
        elif command == "pause":
            self.state = "paused"
        elif command == "reduce_volume":
            self.state = "low_volume"
        elif command == "turn_off":
            self.state = "off"
        else:
            print(f"[AUDIO] Unknown command received: {command}")
            return

        print(f"[AUDIO] Audio system is now: {self.state.upper()}")
        self.publish_status()


if __name__ == "__main__":
    mqtt = create_mqtt_client()
    mqtt.loop_start()

    audio = AudioSystem(mqtt_client=mqtt)
