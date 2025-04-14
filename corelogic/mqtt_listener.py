"""
Module: corelogic/mqtt_listener.py
Purpose: Subscribes to sensor MQTT topics, evaluates rules, and triggers device actions.
Author: Itay Vazana
"""

import os
import json
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from corelogic.rule_engine import RuleEngine
from corelogic.devices_registry import get_all_devices
from corelogic.mqtt_publisher import MQTTPublisher

# Load environment variables
load_dotenv()
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", 60))

# Global sensor state memory
sensor_state = {}

# Initialize core components
rule_engine = RuleEngine()
devices = get_all_devices()
mqtt_publisher = MQTTPublisher()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT connected. Subscribing to sensor topics...")
        client.subscribe("sensor/#")
    else:
        print(f"❌ MQTT connection failed with code {rc}")


def on_message(client, userdata, msg):
    try:
        sensor_id = msg.topic.split("sensor/")[-1]
        payload = json.loads(msg.payload.decode("utf-8"))
        value = payload.get("value")
        if sensor_id and value is not None:
            sensor_state[sensor_id] = value
            print(f"📥 Received sensor: {sensor_id} → {value}")

            # Evaluate rules based on updated state
            triggered_rules = rule_engine.evaluate_rules(sensor_state)
            for rule in triggered_rules:
                for action in rule["actions"]:
                    device_id = action["device_id"]
                    command = action["command"]
                    device = devices.get(device_id)
                    if device:
                        print(f"⚙️  Triggering device: {device_id} via rule: {rule['rule_id']}")
                        device.apply_state(mqtt_publisher.client, command)
    except Exception as e:
        print(f"⚠️ Error processing MQTT message: {e}")


def start_listener():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
    client.loop_forever()


if __name__ == "__main__":
    start_listener()