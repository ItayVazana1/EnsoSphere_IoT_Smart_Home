from devices.base_device import BaseDevice
import json

class DoorLock(BaseDevice):
    """
    Smart Door Lock device class.

    Manages locking and unlocking the main entrance door.

    Attributes:
        device_id (str): Unique identifier for the lock.
        room (str): The room/location (usually 'Entrance').
        state (str): Lock state ("locked"/"unlocked").
    """

    def __init__(self, device_id: str, room: str, mqtt_client):
        """Initialize the door lock with default 'locked' state and subscribe to MQTT."""
        super().__init__(device_id, room, mqtt_client)
        self.state = "locked"

    def mqtt_callback(self, client, userdata, msg):
        """
        Callback to handle incoming MQTT messages for the door lock.

        Args:
            client (mqtt.Client): The MQTT client instance.
            userdata (Any): User-defined data (not used).
            msg (MQTTMessage): The received message.
        """
        try:
            payload = json.loads(msg.payload.decode())
            command = payload.get("command")
            parameters = payload.get("parameters", {})
            self.receive_command(command, parameters)
        except Exception as e:
            print(f"[MQTT][DoorLock] Failed to process message: {e}")

    def receive_command(self, command: str, parameters: dict = None):
        """
        Handle commands to lock or unlock the door.

        Args:
            command (str): Either 'lock' or 'unlock'.
            parameters (dict, optional): Reserved for future use.

        Raises:
            ValueError: If an unsupported command is received.
        """
        if command == "lock":
            self.lock()
        elif command == "unlock":
            self.unlock()
        else:
            raise ValueError(f"Unsupported command: {command}")

    def lock(self):
        """Lock the door."""
        self.state = "locked"
        print(f"[DoorLock] {self.device_id} in {self.room} is now LOCKED")

    def unlock(self):
        """Unlock the door."""
        self.state = "unlocked"
        print(f"[DoorLock] {self.device_id} in {self.room} is now UNLOCKED")

    @property
    def locked(self):
        """Convenience property to check if the door is locked."""
        return self.state == "locked"

    def get_status(self):
        """
        Return the current state of the door lock.

        Returns:
            dict: Device ID, room, and lock state.
        """
        return {
            "device_id": self.device_id,
            "room": self.room,
            "state": self.state
        }
