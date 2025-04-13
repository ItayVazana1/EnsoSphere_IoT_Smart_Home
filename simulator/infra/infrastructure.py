"""
Module: simulator/infrastructure.py
Purpose: Wrap external services used by the simulator: MQTT, sensor publishing, and DB fetchers.
Author: Itay Vazana
"""

from simulator.infra.mqtt_client import MQTTClient
from simulator.infra.sensor_publisher import SensorPublisher
from simulator.infra.device_state_fetcher import fetch_device_states


class Infrastructure:
    """
    Infrastructure provides access to simulation services like:
    - MQTT client
    - Sensor publisher
    - Device state fetcher (from MySQL)
    """

    def __init__(self):
        self.mqtt = MQTTClient()
        self.publisher = SensorPublisher()

    def get_device_states(self):
        """
        Fetch latest device states from database.

        Returns:
            dict: device_id → state dict
        """
        return fetch_device_states()

    def publish_sensors(self, sensor_outputs: dict):
        """
        Publish all sensor outputs via MQTT.

        Args:
            sensor_outputs (dict): sensor_id → value
        """
        self.publisher.publish_sensor_outputs(sensor_outputs)

    def is_connected(self) -> bool:
        """
        Check MQTT connection status.

        Returns:
            bool
        """
        return self.mqtt.connected

    def shutdown(self):
        """
        Gracefully shut down external connections (e.g., MQTT).
        """
        self.publisher.shutdown()
