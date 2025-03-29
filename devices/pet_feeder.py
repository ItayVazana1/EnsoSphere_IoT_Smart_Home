from devices.base_device import BaseDevice
import time
import json

class PetFeeder(BaseDevice):
    """
    Smart Pet Feeder device class.

    Handles the dispensing of food for pets and tracks usage.

    Attributes:
        device_id (str): Unique identifier for the feeder.
        room (str): Room where the feeder is located.
        state (str): Operational state ("ready", "dispensing").
        dispense_count (int): Number of times food was dispensed today.
    """

    def __init__(self, device_id: str, room: str, mqtt_client):
        """Initialize pet feeder with default state and zero dispense count."""
        super().__init__(device_id, room, mqtt_client)
        self.state = "ready"
        self.dispense_count = 0

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
            print(f"[MQTT][PetFeeder] Failed to process message: {e}")

    def receive_command(self, command: str, parameters: dict = None):
        """
        Handle incoming command to dispense food.

        Args:
            command (str): Command string ("dispense_food").
            parameters (dict, optional): Reserved for future use.

        Raises:
            ValueError: If unsupported command is received.
        """
        if command == "dispense_food":
            self.dispense_food()
        else:
            raise ValueError(f"Unsupported command: {command}")

    def dispense_food(self):
        """
        Dispense food to pet and update internal state.

        Simulates a short dispensing operation.
        """
        self.state = "dispensing"
        print(f"[PetFeeder] {self.device_id} dispensing food in {self.room}")
        time.sleep(0.5)
        self.dispense_count += 1
        self.state = "ready"
        print(f"[PetFeeder] {self.device_id} finished dispensing. Total today: {self.dispense_count}")

    def get_status(self):
        """
        Returns the current status of the pet feeder.

        Returns:
            dict: Includes ID, room, state, and daily dispense count.
        """
        return {
            "device_id": self.device_id,
            "room": self.room,
            "state": self.state,
            "dispense_count": self.dispense_count
        }
