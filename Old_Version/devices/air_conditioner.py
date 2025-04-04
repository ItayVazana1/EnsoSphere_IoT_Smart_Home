from devices.base_device import BaseDevice
import json

class AirConditioner(BaseDevice):
    """
    Smart Air Conditioner device class.

    Controls on/off state and target temperature of the air conditioner.

    Attributes:
        device_id (str): Unique identifier for the AC.
        room (str): The room where the AC is installed.
        state (str): Current state of the AC ("on"/"off").
        target_temperature (float): Desired temperature set by the user.
    """

    def __init__(self, device_id: str, room: str, mqtt_client):
        """Initialize Air Conditioner device with default 'off' state and default temperature."""
        super().__init__(device_id, room, mqtt_client)
        self.state = "off"
        self.target_temperature = 24.0  # Default temperature

    def mqtt_callback(self, client, userdata, msg):
        """
        Callback function triggered when a message is received on the air conditioner MQTT topic.

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
            print(f"[MQTT][AirConditioner] Failed to process message: {e}")

    def receive_command(self, command: str, parameters: dict = None):
        """
        Receives and handles commands for the air conditioner.

        Args:
            command (str): The command ("turn_on"/"turn_off"/"set_temperature").
            parameters (dict, optional): Additional parameters, such as desired temperature.

        Raises:
            ValueError: If the command is unsupported or parameters are missing.
        """
        if command == "turn_on":
            self.turn_on()
        elif command == "turn_off":
            self.turn_off()
        elif command == "set_temperature":
            if parameters and "temperature" in parameters:
                self.set_temperature(parameters["temperature"])
            else:
                raise ValueError("Missing 'temperature' parameter for 'set_temperature' command.")
        else:
            raise ValueError(f"Unsupported command: {command}")

    def turn_on(self):
        """Turn the AC on."""
        self.state = "on"
        print(f"[AirConditioner] {self.device_id} in {self.room} turned ON")

    def turn_off(self):
        """Turn the AC off."""
        self.state = "off"
        print(f"[AirConditioner] {self.device_id} in {self.room} turned OFF")

    def set_temperature(self, temperature: float):
        """
        Set the target temperature for the AC.

        Args:
            temperature (float): Desired temperature value.
        """
        self.target_temperature = temperature
        print(f"[AirConditioner] {self.device_id} temperature set to {temperature}°C")

    def get_status(self):
        """
        Returns the current status of the AC.

        Returns:
            dict: Device status including ID, room, state, and target temperature.
        """
        return {
            "device_id": self.device_id,
            "room": self.room,
            "state": self.state,
            "target_temperature": self.target_temperature
        }