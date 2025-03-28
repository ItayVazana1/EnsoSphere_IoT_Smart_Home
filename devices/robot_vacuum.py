from devices.base_device import BaseDevice

class RobotVacuum(BaseDevice):
    """
    Smart Robot Vacuum device class.

    Controls cleaning status and navigation of the robot vacuum.

    Attributes:
        device_id (str): Unique identifier for the robot.
        room (str): The default room where the robot starts.
        state (str): Power state ("on"/"off").
        mode (str): Current activity ("idle", "cleaning", "charging").
    """

    def __init__(self, device_id: str, room: str):
        """Initialize Robot Vacuum with default 'off' state and 'idle' mode."""
        super().__init__(device_id, room)
        self.state = "off"
        self.mode = "idle"

    def receive_command(self, command: str, parameters: dict = None):
        """
        Receives and handles commands for the robot vacuum.

        Args:
            command (str): Command string ("start_cleaning", "stop_cleaning", "go_home").
            parameters (dict, optional): Reserved for future use.

        Raises:
            ValueError: If the command is unsupported.
        """
        if command == "start_cleaning":
            self.start_cleaning()
        elif command == "stop_cleaning":
            self.stop_cleaning()
        elif command == "go_home":
            self.go_home()
        else:
            raise ValueError(f"Unsupported command: {command}")

    def start_cleaning(self):
        """Start cleaning operation."""
        self.state = "on"
        self.mode = "cleaning"

    def stop_cleaning(self):
        """Stop cleaning operation and go idle."""
        self.state = "on"
        self.mode = "idle"

    def go_home(self):
        """Send robot back to charging station."""
        self.state = "off"
        self.mode = "charging"

    def get_status(self):
        """
        Returns the current status of the robot vacuum.

        Returns:
            dict: Device status including ID, room, power state, and mode.
        """
        return {
            "device_id": self.device_id,
            "room": self.room,
            "state": self.state,
            "mode": self.mode
        }
