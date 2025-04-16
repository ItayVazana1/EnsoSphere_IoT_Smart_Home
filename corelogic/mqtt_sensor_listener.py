"""
Module: corelogic/mqtt_sensor_listener.py
Purpose: Listens to MQTT sensor messages and stores latest values for CoreLogic tick-based processing.
Author: Itay Vazana
"""

import json
import threading
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", 60))


class MQTTSensorListener:
    """
    Shared listener for MQTT sensor updates.
    Stores latest values per sensor_id for CoreLogic rule evaluation.
    """

    def __init__(self):
        self.client = mqtt.Client()
        self.latest_values = {}  # {sensor_id: value}
        self.lock = threading.Lock()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def start(self):
        """
        Connect to broker and begin listening loop in a background thread.
        """
        self.client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        thread = threading.Thread(target=self.client.loop_forever, daemon=True)
        thread.start()
        print("[MQTT Listener] Started and listening to sensor/#")

    def on_connect(self, client, userdata, flags, rc):
        """
        Subscribes to all sensor topics.
        """
        if rc == 0:
            print("[MQTT Listener] Connected successfully. Subscribing to sensor/#")
            client.subscribe("sensor/#")
        else:
            print(f"[MQTT Listener] Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        """
        Stores incoming sensor values in internal dictionary.
        """
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            sensor_id = msg.topic.split("sensor/")[-1]
            value = payload.get("value")
            if sensor_id and value is not None:
                with self.lock:
                    self.latest_values[sensor_id] = value
                print(f"[MQTT Listener] Sensor update: {sensor_id} → {value}")
        except Exception as e:
            print(f"[MQTT Listener] Failed to process message: {e}")

    def get_latest_value(self, sensor_id: str):
        """
        Retrieves the latest value for a specific sensor.
        Returns None if not found.
        """
        with self.lock:
            return self.latest_values.get(sensor_id)

    def get_all_latest_values(self):
        """
        Returns a shallow copy of the full sensor state.
        """
        with self.lock:
            return dict(self.latest_values)
