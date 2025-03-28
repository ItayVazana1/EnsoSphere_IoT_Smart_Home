from devices.base_device import BaseDevice

class Blinds(BaseDevice):
    """
    Smart Blinds device class.

    Controls opening and closing of blinds in a specific room.

    Attributes:
        device_id (str): Unique identifier for the blinds.
        room (str): The room where the blinds are installed.
        state (str): Current state of the blinds ("open"/"closed").
    """

    def __init__(self, device_id: str, room: str):
        """Initialize Blinds device with default 'closed' state."""
        super().__init__(device_id, room)
        self.state = "closed"

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

    def close(self):
        """Closes the blinds."""
        self.state = "closed"

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
