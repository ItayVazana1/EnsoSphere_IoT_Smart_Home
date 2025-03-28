import pytest
from devices.base_device import BaseDevice
from sensors.base_sensor import BaseSensor

# Dummy subclass for testing BaseDevice
class DummyDevice(BaseDevice):
    def receive_command(self, command, parameters=None):
        if command == "turn_on":
            self.state = "on"
        elif command == "turn_off":
            self.state = "off"

# Dummy subclass for testing BaseSensor
class DummySensor(BaseSensor):
    def read_value(self):
        self.last_value = 42
        return self.last_value

# Tests for BaseDevice
def test_base_device():
    device = DummyDevice("device_01", "Living Room")
    assert device.get_status() == {"device_id": "device_01", "room": "Living Room", "state": "off"}

    device.receive_command("turn_on")
    assert device.state == "on"

    device.receive_command("turn_off")
    assert device.state == "off"

# Tests for BaseSensor
def test_base_sensor():
    sensor = DummySensor("sensor_01", "Kitchen")
    assert sensor.get_data() == {"sensor_id": "sensor_01", "room": "Kitchen", "value": None}

    value = sensor.read_value()
    assert value == 42
    assert sensor.get_data()["value"] == 42

