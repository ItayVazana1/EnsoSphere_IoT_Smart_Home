from devices.base_device import BaseDevice
import json

class SecuritySystem(BaseDevice):
    """
    Smart Security System device class.

    Supports arming, disarming, and triggering alerts.

    Attributes:
        device_id (str): Unique identifier.
        room (str): Typically 'Entrance' or 'Entire Home'.
        state (str): "armed", "disarmed", or "alert".
    """

    def __init__(self, device_id: str, room: str, mqtt_client):
        """Initialize security system in disarmed state."""
        super().__init__(device_id, room, mqtt_client)
        self.state = "disarmed"

    def mqtt_callback(self, client, userdata, msg):
        """Handle incoming MQTT messages for security commands."""
        try:
            payload = json.loads(msg.payload.decode())
            command = payload.get("command")
            self.receive_command(command)
        except Exception as e:
            print(f"[MQTT][SecuritySystem] Failed to process message: {e}")

    def receive_command(self, command: str, parameters: dict = None):
        """Process security commands."""
        if command == "arm":
            self.arm()
        elif command == "disarm":
            self.disarm()
        elif command == "alert":
            self.trigger_alert()
        else:
            raise ValueError(f"Unsupported command: {command}")

    def arm(self):
        self.state = "armed"
        print(f"[SecuritySystem] {self.device_id} is now ARMED in {self.room}")

    def disarm(self):
        self.state = "disarmed"
        print(f"[SecuritySystem] {self.device_id} is now DISARMED in {self.room}")

    def trigger_alert(self):
        self.state = "alert"
        print(f"[SecuritySystem] ALERT TRIGGERED by {self.device_id} in {self.room}")

    def get_status(self):
        """Return system status."""
        return {
            "device_id": self.device_id,
            "room": self.room,
            "state": self.state
        }
