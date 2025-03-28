from devices.base_device import BaseDevice

class Lights(BaseDevice):
    """
    Smart Lights device class.

    Controls and monitors the state of lighting devices in a room.

    Attributes:
        device_id (str): Unique identifier for the lights.
        room (str): The room where the lights are installed.
        state (str): Current state of the lights ("on"/"off").
    """

    def __init__(self, device_id: str, room: str):
        """Initialize Lights device with default 'off' state."""
        super().__init__(device_id, room)

    def receive_command(self, command: str, parameters: dict = None):
        """
        Receives and handles commands for lights.

        Args:
            command (str): The command to perform ("turn_on" / "turn_off").
            parameters (dict, optional): Additional parameters for future expansion.

        Raises:
            ValueError: If the command is unsupported.
        """
        if command == "turn_on":
            self.turn_on()
        elif command == "turn_off":
            self.turn_off()
        else:
            raise ValueError(f"Unsupported command: {command}")

    def turn_on(self):
        """Turn the lights on."""
        self.state = "on"

    def turn_off(self):
        """Turn the lights off."""
        self.state = "off"

    def get_status(self):
        """
        Returns the current status of the lights.

        Returns:
            dict: Device status including ID, room, and current state.
        """
        return {
            "device_id": self.device_id,
            "room": self.room,
            "state": self.state
        }
