from devices.base_device import BaseDevice

class DoorLock(BaseDevice):
    """
    Smart Door Lock device class.

    Manages locking and unlocking the main entrance door.

    Attributes:
        device_id (str): Unique identifier for the lock.
        room (str): The room/location (usually 'Entrance').
        state (str): Lock state ("locked"/"unlocked").
    """

    def __init__(self, device_id: str, room: str):
        """Initialize the door lock with default 'locked' state."""
        super().__init__(device_id, room)
        self.state = "locked"

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

    def unlock(self):
        """Unlock the door."""
        self.state = "unlocked"

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
