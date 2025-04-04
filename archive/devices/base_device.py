import json
from datetime import datetime


class BaseDevice:
    """
    Base class for all actuators (devices) in the Smart Apartment IoT system.

    Attributes:
        device_id (str): Unique identifier for the device.
        room (str): The room where the device is located.
        state (str): Current state of the device (e.g., "on", "off").
    """

    def __init__(self, device_id: str, room: str, mqtt_client=None):
        self.device_id = device_id
        self.room = room
        self.state = "off"
        self.mqtt_client = mqtt_client

        if self.mqtt_client:
            self.subscribe_to_commands()

    def get_command_topic(self) -> str:
        """
        Returns the MQTT topic used to receive commands.
        Format: MyHome/<room>/<device_type>/<device_id>
        """
        device_type = self.__class__.__name__.lower()
        return f"MyHome/{self.room}/{device_type}/{self.device_id}"

    def get_status_topic(self) -> str:
        """
        Returns the MQTT topic used to publish status updates.
        """
        device_type = self.__class__.__name__.lower()
        return f"MyHome/{self.room}/{device_type}/{self.device_id}/status"

    def subscribe_to_commands(self):
        """
        Subscribes to the device's MQTT command topic.
        """
        topic = self.get_command_topic()
        self.mqtt_client.subscribe(topic)
        self.mqtt_client.message_callback_add(topic, self.mqtt_callback)
        print(f"[MQTT][{self.__class__.__name__}] Subscribed to {topic}")

    def mqtt_callback(self, client, userdata, msg):
        """
        Handles incoming MQTT messages and extracts the command.
        """
        try:
            payload = json.loads(msg.payload.decode())
            command = payload.get("command")
            parameters = payload.get("parameters", {})
            print(f"[MQTT][{self.device_id}] Received command: {command}")
            self.receive_command(command, parameters)
        except Exception as e:
            print(f"[ERROR][{self.device_id}] Failed to handle MQTT message: {e}")

    def receive_command(self, command: str, parameters: dict = None):
        """
        This method should be implemented by subclasses to execute received commands.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def publish_status(self):
        """
        Publishes the current state to the MQTT status topic.
        """
        if not self.mqtt_client:
            return

        topic = self.get_status_topic()
        payload = {
            "device_id": self.device_id,
            "room": self.room,
            "state": self.state,
            "timestamp": datetime.now().isoformat()
        }
        self.mqtt_client.publish(topic, json.dumps(payload))
        print(f"[MQTT][{self.device_id}] Status published to '{topic}': {payload}")
