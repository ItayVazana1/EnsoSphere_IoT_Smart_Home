import pytest
import time
import json

from core import mqtt_client as mqtt_module
from core.environment_manager import EnvironmentManager

# Sensor imports
from sensors.motion_sensor import MotionSensor
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.gas_sensor import GasSensor
from sensors.noise_sensor import NoiseSensor


# ---------- Fixtures ----------

@pytest.fixture(scope="module")
def mqtt_client():
    client = mqtt_module.create_mqtt_client()
    client.loop_start()
    for _ in range(50):
        if client.is_connected():
            break
        time.sleep(0.1)
    else:
        pytest.fail("MQTT client failed to connect.")
    yield client
    client.loop_stop()
    client.disconnect()


@pytest.fixture(scope="module")
def env_manager():
    return EnvironmentManager()


# ---------- Sensor Tests ----------

class TestMotionSensor:
    def test_publish(self, mqtt_client):
        sensor = MotionSensor("MOTION_01", "living_room", mqtt_client=mqtt_client)
        sensor.publish_value()
        assert sensor.last_value in ["detected", "none"]


class TestTemperatureSensor:
    def test_publish(self, mqtt_client, env_manager, capsys):
        sensor = TemperatureSensor("TEMP_01", "kitchen", mqtt_client=mqtt_client, env_manager=env_manager)
        sensor.publish_value()
        time.sleep(1)
        out = capsys.readouterr().out
        assert "MyHome/kitchen/temperaturesensor/TEMP_01" in out
        assert '"sensor_id": "TEMP_01"' in out
        assert '"room": "kitchen"' in out
        assert '"value":' in out
        assert '"timestamp":' in out


class TestHumiditySensor:
    def test_publish(self, mqtt_client, env_manager, capsys):
        sensor = HumiditySensor("HUM_01", "bathroom", mqtt_client=mqtt_client, env_manager=env_manager)
        sensor.publish_value()
        time.sleep(1)
        out = capsys.readouterr().out
        assert "MyHome/bathroom/humiditysensor/HUM_01" in out
        assert '"sensor_id": "HUM_01"' in out
        assert '"room": "bathroom"' in out
        assert '"value":' in out
        assert '"timestamp":' in out


class TestGasSensor:
    def test_publish(self, mqtt_client, env_manager, capsys):
        """
        Test that the GasSensor publishes simulated gas readings via MQTT.
        """
        sensor = GasSensor("GAS_01", "bathroom", mqtt_client=mqtt_client, env_manager=env_manager)
        sensor.publish_value()
        time.sleep(1)  # give time for MQTT publish to be processed

        output = capsys.readouterr().out
        assert "MyHome/bathroom/gassensor/GAS_01" in output
        assert '"sensor_id": "GAS_01"' in output
        assert '"room": "bathroom"' in output
        assert '"value":' in output
        assert '"timestamp":' in output


class TestNoiseSensor:
    def test_publish(self, mqtt_client, env_manager, capsys):
        """
        Test that the NoiseSensor reads and publishes noise level correctly via MQTT.
        """
        sensor = NoiseSensor("NOISE_01", "bedroom", mqtt_client=mqtt_client, env_manager=env_manager)
        sensor.publish_value()
        time.sleep(1)

        out = capsys.readouterr().out
        assert "MyHome/bedroom/noisesensor/NOISE_01" in out
        assert '"sensor_id": "NOISE_01"' in out
        assert '"room": "bedroom"' in out
        assert '"value":' in out
        assert '"timestamp":' in out

        # Optional: validate value range
        value = sensor.last_value
        assert 30.0 <= value <= 90.0
