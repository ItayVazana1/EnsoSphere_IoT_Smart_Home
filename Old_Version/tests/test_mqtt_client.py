from core import mqtt_client as mqtt_module
import time
import pytest

@pytest.fixture
def mqtt_client():
    client = mqtt_module.create_mqtt_client()
    client.loop_start()

    # Wait for connection
    for _ in range(50):
        if client.is_connected():
            break
        time.sleep(0.1)
    else:
        client.loop_stop()
        client.disconnect()
        pytest.fail("MQTT client failed to connect.")

    yield client

    client.loop_stop()
    client.disconnect()


def test_broker_connection(mqtt_client):
    """Test if MQTT client connects successfully to the broker."""
    assert mqtt_client.is_connected(), "Client should be connected."


def test_publish_message(mqtt_client):
    """Test publishing a message to a realistic topic."""
    room, device_type, device_id, payload = "living_room", "lights", "LIGHT_01", "ON"
    result, mid = mqtt_module.publish_message(mqtt_client, room, device_type, device_id, payload)
    assert result == 0, f"Publish failed with result code: {result}"


def test_subscribe_to_topic(mqtt_client):
    """Test subscribing to a realistic device topic."""
    room, device_type, device_id = "bedroom", "blinds", "BLIND_01"
    result, mid = mqtt_module.subscribe_to_device(mqtt_client, room, device_type, device_id)
    assert result == 0, f"Subscribe failed with result code: {result}"


def test_invalid_broker_connection():
    """Test connection handling with incorrect broker details."""
    original_host = mqtt_module.BROKER_HOST
    mqtt_module.BROKER_HOST = "invalid_host"

    with pytest.raises(Exception):
        client = mqtt_module.create_mqtt_client()
        client.loop_start()
        time.sleep(2)
        client.loop_stop()
        client.disconnect()

    mqtt_module.BROKER_HOST = original_host


def test_topic_format(mqtt_client):
    """Test that the MQTT topic is correctly formatted."""
    room, device_type, device_id = "kitchen", "temperature_sensor", "TEMP_01"
    expected_topic = f"{mqtt_module.BASE_TOPIC}/{room}/{device_type}/{device_id}"

    def mock_publish(topic, payload):
        assert topic == expected_topic, f"Topic format incorrect: {topic}"
        return 0, 1

    mqtt_client.publish = mock_publish

    mqtt_module.publish_message(mqtt_client, room, device_type, device_id, "22.3")


def test_json_payload_handling(mqtt_client):
    """Test sending and receiving a JSON formatted payload."""
    import json

    room, device_type, device_id = "bathroom", "humidity_sensor", "HUM_01"
    payload = json.dumps({"humidity": 55.2})

    result, mid = mqtt_module.publish_message(mqtt_client, room, device_type, device_id, payload)
    assert result == 0, f"JSON payload publish failed with result code: {result}"
