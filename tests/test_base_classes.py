import pytest
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
    device = DummyDevice("dev_01", "Living Room")
    assert device.device_id == "dev_01"
    assert device.room == "Living Room"
    assert device.state == "off"

def test_base_device_receive_command_override():
    device = DummyDevice("dev_01", "Living Room")
    device.receive_command("activate")
    assert device.state == "received: activate"

def test_base_device_status():
    device = DummyDevice("dev_01", "Living Room")
    status = device.get_status()
    assert status == {
        "device_id": "dev_01",
        "room": "Living Room",
        "state": "off"
    }


# ---------- Tests for BaseSensor ----------

def test_base_sensor_init():
    sensor = DummySensor("sensor_01", "Kitchen")
    assert sensor.sensor_id == "sensor_01"
    assert sensor.room == "Kitchen"
    assert sensor.last_value is None

def test_base_sensor_read_value_override():
    sensor = DummySensor("sensor_01", "Kitchen")
    value = sensor.read_value()
    assert value == 42
    assert sensor.last_value == 42

def test_base_sensor_data_structure():
    sensor = DummySensor("sensor_01", "Kitchen")
    sensor.read_value()
    data = sensor.get_data()
    assert data == {
        "sensor_id": "sensor_01",
        "room": "Kitchen",
        "value": 42
    }
