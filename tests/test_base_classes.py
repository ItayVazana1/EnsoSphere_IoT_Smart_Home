import pytest
from datetime import datetime
from devices.base_device import BaseDevice
from sensors.base_sensor import BaseSensor


# ---------- Dummy Classes for Testing ----------

class DummyDevice(BaseDevice):
    def receive_command(self, command: str, parameters: dict = None):
        self.state = f"received: {command}"


class DummySensor(BaseSensor):
    def read_value(self):
        self.last_value = 42
        return self.last_value


# ---------- Tests for BaseDevice ----------

def test_base_device_init():
    """Test initialization of a BaseDevice-derived class."""
    device = DummyDevice("dev_01", "Living Room")
    assert device.device_id == "dev_01"
    assert device.room == "Living Room"
    assert device.state == "off"


def test_base_device_receive_command_override():
    """Test that receive_command() is overridden and sets custom state."""
    device = DummyDevice("dev_01", "Living Room")
    device.receive_command("activate")
    assert device.state == "received: activate"


def test_base_device_status():
    """Test the get_status() method of a BaseDevice."""
    device = DummyDevice("dev_01", "Living Room")
    status = device.get_status()
    assert status == {
        "device_id": "dev_01",
        "room": "Living Room",
        "state": "off"
    }


# ---------- Tests for BaseSensor ----------

def test_base_sensor_init():
    """Test initialization of a BaseSensor-derived class."""
    sensor = DummySensor("sensor_01", "Kitchen")
    assert sensor.sensor_id == "sensor_01"
    assert sensor.room == "Kitchen"
    assert sensor.last_value is None


def test_base_sensor_read_value_override():
    """Test that read_value() is overridden and returns expected value."""
    sensor = DummySensor("sensor_01", "Kitchen")
    value = sensor.read_value()
    assert value == 42
    assert sensor.last_value == 42


def test_base_sensor_data_structure():
    """Test get_data() structure after reading value."""
    sensor = DummySensor("sensor_01", "Kitchen")
    sensor.read_value()
    data = sensor.get_data()
    assert data == {
        "sensor_id": "sensor_01",
        "room": "Kitchen",
        "value": 42
    }


def test_base_sensor_publish_value_structure(monkeypatch):
    """
    Test that publish_value() builds the correct MQTT payload and topic format.
    """

    class DummyEnv:
        simulated_time = datetime(2025, 1, 1, 12, 0, 0)

    class DummySensorWithEnv(BaseSensor):
        def read_value(self):
            self.last_value = 100
            return self.last_value

    sensor = DummySensorWithEnv("sensor_01", "Living Room")
    sensor.env_manager = DummyEnv()

    published_data = {}

    class DummyMQTT:
        def publish(self, topic, payload):
            published_data["topic"] = topic
            published_data["payload"] = payload

    sensor.mqtt_client = DummyMQTT()
    sensor.publish_value()

    assert published_data["topic"] == "MyHome/Living Room/dummysensorwithenv/sensor_01"
    assert '"sensor_id": "sensor_01"' in published_data["payload"]
    assert '"room": "Living Room"' in published_data["payload"]
    assert '"value": 100' in published_data["payload"]
    assert '"timestamp": "2025-01-01T12:00:00"' in published_data["payload"]
