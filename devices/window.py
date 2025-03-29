from devices.base_device import BaseDevice
import json

class Window(BaseDevice):
    """
    Smart Window device class.

    Controls opening and closing of a window in a room.

    Attributes:
        device_id (str): Unique identifier for the window.
        room (str): The room where the window is installed.
        state (str): Current state ("open" or "closed").
    """

    def __init__(self, device_id: str, room: str, mqtt_client):
        """Initialize the window as closed."""
        super().__init__(device_id, room, mqtt_client)
        self.state = "closed"

    def mqtt_callback(self, client, userdata, msg):
        """Handle incoming MQTT messages."""
        try:
            payload = json.loads(msg.payload.decode())
            command = payload.get("command")
            self.receive_command(command)
        except Exception as e:
            print(f"[MQTT][Window] Failed to process message: {e}")

    def receive_command(self, command: str, parameters: dict = None):
        """Process 'open' or 'close' commands."""
        if command == "open":
            self.open()
        elif command == "close":
            self.close()
        else:
            raise ValueError(f"Unsupported command: {command}")

    def open(self):
        """Open the window."""
        self.state = "open"
        print(f"[Window] {self.device_id} in {self.room} opened")

    def close(self):
        """Close the window."""
        self.state = "closed"
        print(f"[Window] {self.device_id} in {self.room} closed")

    def get_status(self):
        """Return the window's current status."""
        return {
            "device_id": self.device_id,
            "room": self.room,
            "state": self.state
        }
