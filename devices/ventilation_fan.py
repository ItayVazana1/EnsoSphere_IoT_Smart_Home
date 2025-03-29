from devices.base_device import BaseDevice
import json

class VentilationFan(BaseDevice):
    """
    Smart Ventilation Fan device class.

    Controls a fan for ventilation in the bathroom.

    Attributes:
        device_id (str): Unique identifier for the fan.
        room (str): The room where the fan is installed.
        state (str): Current state of the fan ("on"/"off").
    """

    def __init__(self, device_id: str, room: str, mqtt_client):
        """Initialize the fan in the 'off' state."""
        super().__init__(device_id, room, mqtt_client)
        self.state = "off"

    def mqtt_callback(self, client, userdata, msg):
        """
        Callback triggered when a command is received via MQTT.

        Args:
            msg (MQTTMessage): Contains the command and optional parameters.
        """
        try:
            payload = json.loads(msg.payload.decode())
            command = payload.get("command")
            self.receive_command(command)
        except Exception as e:
            print(f"[MQTT][VentilationFan] Failed to process message: {e}")

    def receive_command(self, command: str, parameters: dict = None):
        """
        Executes a command such as 'turn_on' or 'turn_off'.

        Args:
            command (str): The command string.
        """
        if command == "turn_on":
            self.turn_on()
        elif command == "turn_off":
            self.turn_off()
        else:
            raise ValueError(f"Unsupported command: {command}")

    def turn_on(self):
        """Activate the ventilation fan."""
        self.state = "on"
        print(f"[VentilationFan] {self.device_id} in {self.room} turned ON")

    def turn_off(self):
        """Deactivate the ventilation fan."""
        self.state = "off"
        print(f"[VentilationFan] {self.device_id} in {self.room} turned OFF")

    def get_status(self):
        """Return current state of the fan."""
        return {
            "device_id": self.device_id,
            "room": self.room,
            "state": self.state
        }
