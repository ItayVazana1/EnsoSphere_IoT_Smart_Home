from core import mqtt_client as mqtt_module
import time

def test_mqtt_connection_and_publish():
    """
    Integration test for MQTT client:
    - Connects to the broker
    - Waits for connection to be established
    - Publishes a test message
    - Asserts that publish returns success
    """
    client = mqtt_module.create_mqtt_client()
    client.loop_start()

    # Wait for connection (up to 5 seconds)
    for _ in range(50):  # 0.1 * 50 = 5 seconds
        if client.is_connected():
            break
        time.sleep(0.1)
    else:
        client.loop_stop()
        client.disconnect()
        assert False, "MQTT client failed to connect within timeout."

    test_topic = "test/topic"
    test_payload = "Test from pytest"
    result = client.publish(test_topic, test_payload)
    assert result.rc == 0, f"Publish failed with return code: {result.rc}"

    time.sleep(1)  # Allow time for the message to be processed
    client.loop_stop()
    client.disconnect()