from devices.base_device import BaseDevice
import json

class Blinds(BaseDevice):
    """
    Smart Blinds device class.

    Controls opening and closing of blinds in a specific room.

    Attributes:
        device_id (str): Unique identifier for the blinds.
        room (str): The room where the blinds are installed.
        state (str): Current state of the blinds ("open"/"closed").
    """

    def __init__(self, device_id: str, room: str, mqtt_client):
        """Initialize Blinds device with default 'closed' state and MQTT support."""
        super().__init__(device_id, room, mqtt_client)
        self.state = "closed"

    def mqtt_callback(self, client, userdata, msg):
        """
        Callback function triggered when a message is received on the blinds MQTT topic.

        Args:
            client (mqtt.Client): The MQTT client instance.
            userdata (Any): User-defined data (not used).
            msg (MQTTMessage): The received message object containing topic and payload.
        """
        try:
            payload = json.loads(msg.payload.decode())
            command = payload.get("command")
            parameters = payload.get("parameters", {})
            self.receive_command(command, parameters)
        except Exception as e:
            print(f"[MQTT][Blinds] Failed to process message: {e}")

    def receive_command(self, command: str, parameters: dict = None):
        """
        Receives and handles commands for blinds.

        Args:
            command (str): The command to perform ("open" / "close").
            parameters (dict, optional): Additional parameters for future expansion.

        Raises:
            ValueError: If the command is unsupported.
        """
        if command == "open":
            self.open()
        elif command == "close":
            self.close()
        else:
            raise ValueError(f"Unsupported command: {command}")

    def open(self):
        """Opens the blinds."""
        self.state = "open"
        print(f"[Blinds] {self.device_id} in {self.room} opened")

    def close(self):
        """Closes the blinds."""
        self.state = "closed"
        print(f"[Blinds] {self.device_id} in {self.room} closed")

    def get_status(self):
        """
        Returns the current status of the blinds.

        Returns:
            dict: Device status including ID, room, and current state.
        """
        return {
            "device_id": self.device_id,
            "room": self.room,
            "state": self.state
        }