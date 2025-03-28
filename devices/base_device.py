

class BaseDevice:
    """
    Base class for all actuators (devices) in the Smart Apartment IoT system.

    Attributes:
        device_id (str): Unique identifier for the device.
        room (str): The room where the device is located.
        state (str): Current state of the device ("on" or "off").
    """

    def __init__(self, device_id: str, room: str):
        """Initialize the base device with its ID and room location."""
        self.device_id = device_id
        self.room = room
        self.state = "off"

    def receive_command(self, command: str, parameters: dict = None):
        """
        Handle incoming commands via MQTT.

        Args:
            command (str): Command to perform (e.g., "turn_on", "turn_off").
            parameters (dict, optional): Additional parameters for the command.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_status(self):
        """Return the current state of the device."""
        return {"device_id": self.device_id, "room": self.room, "state": self.state}
