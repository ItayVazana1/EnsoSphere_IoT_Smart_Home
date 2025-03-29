import yaml
import paho.mqtt.client as mqtt
import time
import uuid

# Load MQTT configuration from config.yaml
with open("../config.yaml", "r") as file:
    config = yaml.safe_load(file)

mqtt_config = config["mqtt"]
BROKER_HOST = mqtt_config["host"]
BROKER_PORT = mqtt_config["port"]
BASE_CLIENT_ID = mqtt_config["client_id"]
KEEPALIVE = mqtt_config["keepalive"]
BASE_TOPIC = mqtt_config["base_topic"]


def on_connect(client, userdata, flags, rc):
    """
    Callback function triggered when the client connects to the MQTT broker.

    Args:
        client (mqtt.Client): The MQTT client instance.
        userdata (Any): User-defined data (not used).
        flags (Dict): Response flags sent by the broker.
        rc (int): Connection result code (0 indicates success).
    """
    if rc == 0:
        print("[MQTT] Connected successfully to broker.")
    else:
        print(f"[MQTT] Connection failed with code {rc}.")


def on_message(client, userdata, msg):
    """
    Callback function triggered when a message is received on a subscribed topic.

    Args:
        client (mqtt.Client): The MQTT client instance.
        userdata (Any): User-defined data (not used).
        msg (MQTTMessage): The received message object containing topic and payload.
    """
    print(f"[MQTT] Message received on topic '{msg.topic}': {msg.payload.decode()}")


def create_mqtt_client():
    """
    Creates and configures the MQTT client with appropriate callbacks.
    Generates a unique client ID to avoid broker conflicts.

    Returns:
        mqtt.Client: Configured MQTT client instance.
    """
    unique_client_id = f"{BASE_CLIENT_ID}_{uuid.uuid4()}"
    client = mqtt.Client(client_id=unique_client_id, protocol=mqtt.MQTTv311, clean_session=True)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT, KEEPALIVE)
    return client


def publish_message(client, room, device_type, device_id, payload):
    """
    Publishes a message to a specified topic based on room, device type, and device ID.

    Args:
        client (mqtt.Client): The MQTT client instance.
        room (str): The room name (e.g., kitchen, living_room).
        device_type (str): The type of the device (e.g., temperature_sensor, lights).
        device_id (str): The unique ID of the device.
        payload (str): The message payload to publish.
    """
    topic = f"{BASE_TOPIC}/{room}/{device_type}/{device_id}"
    result = client.publish(topic, payload)
    print(f"[MQTT] Published to '{topic}': {payload}")
    return result


def subscribe_to_device(client, room, device_type, device_id):
    """
    Subscribes the MQTT client to a specific device topic.

    Args:
        client (mqtt.Client): The MQTT client instance.
        room (str): The room name.
        device_type (str): The type of the device.
        device_id (str): The unique ID of the device.
    """
    topic = f"{BASE_TOPIC}/{room}/{device_type}/{device_id}"
    result = client.subscribe(topic)
    print(f"[MQTT] Subscribed to topic '{topic}'")
    return result


# Example usage
def test_publish_and_subscribe(client):
    room = "kitchen"
    device_type = "temperature_sensor"
    device_id = "TEMP_01"
    payload = "24.7"

    subscribe_to_device(client, room, device_type, device_id)
    time.sleep(1)  # Allow subscription to complete

    publish_message(client, room, device_type, device_id, payload)


if __name__ == "__main__":
    mqtt_client = create_mqtt_client()
    mqtt_client.loop_start()

    test_publish_and_subscribe(mqtt_client)

    time.sleep(5)  # Wait to ensure the message is received

    mqtt_client.loop_stop()
    mqtt_client.disconnect()