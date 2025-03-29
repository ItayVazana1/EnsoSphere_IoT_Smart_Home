class BaseDevice:
    """
    Base class for all actuators (devices) in the Smart Apartment IoT system.

    Attributes:
        device_id (str): Unique identifier for the device.
        room (str): The room where the device is located.
        state (str): Current state of the device ("on" or "off").
    """

    def __init__(self, device_id: str, room: str, mqtt_client=None):
        """Initialize the base device with its ID, room, and optional MQTT client."""
        self.device_id = device_id
        self.room = room
        self.state = "off"
        self.mqtt_client = mqtt_client

        if self.mqtt_client:
            self.subscribe_to_commands()

    def subscribe_to_commands(self):
        """Subscribe to MQTT topic if mqtt_client is provided."""
        topic = f"MyHome/{self.room}/{self.__class__.__name__.lower()}/{self.device_id}"
        self.mqtt_client.subscribe(topic)
        self.mqtt_client.message_callback_add(topic, self.mqtt_callback)
        print(f"[MQTT][{self.__class__.__name__}] Subscribed to {topic}")

    def mqtt_callback(self, client, userdata, msg):
        """Handle incoming MQTT messages (to be implemented by subclasses)."""
        raise NotImplementedError("This method should be overridden by subclasses.")

    def receive_command(self, command: str, parameters: dict = None):
        """Handle incoming commands (to be implemented by subclasses)."""
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_status(self):
        """Return the current state of the device."""
        return {"device_id": self.device_id, "room": self.room, "state": self.state}
