from devices.base_device import BaseDevice
import json

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

    def __init__(self, device_id: str, room: str, mqtt_client):
        """Initialize Robot Vacuum with default 'off' state and 'idle' mode."""
        super().__init__(device_id, room, mqtt_client)
        self.state = "off"
        self.mode = "idle"

    def mqtt_callback(self, client, userdata, msg):
        """
        Handles incoming MQTT messages and delegates commands.

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
            print(f"[MQTT][RobotVacuum] Failed to process message: {e}")

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
        print(f"[RobotVacuum] {self.device_id} started cleaning in {self.room}")

    def stop_cleaning(self):
        """Stop cleaning operation and go idle."""
        self.state = "on"
        self.mode = "idle"
        print(f"[RobotVacuum] {self.device_id} stopped cleaning and is idle in {self.room}")

    def go_home(self):
        """Send robot back to charging station."""
        self.state = "off"
        self.mode = "charging"
        print(f"[RobotVacuum] {self.device_id} returning to dock in {self.room}")

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