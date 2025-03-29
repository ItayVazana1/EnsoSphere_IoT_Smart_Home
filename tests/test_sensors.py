from core.environment_manager import EnvironmentManager
from sensors.temperature_sensor import TemperatureSensor
from sensors.motion_sensor import MotionSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.gas_sensor import GasSensor
from sensors.noise_sensor import NoiseSensor


def test_temperature_sensor():
    """Test the Temperature Sensor functionality."""
    env = EnvironmentManager()
    sensor = TemperatureSensor("temp_01", "Living Room", env)

    value = sensor.read_value()
    assert isinstance(value, float), "Temperature should be a float."
    assert 0 <= value <= 50, "Temperature should be within a realistic range."

    data = sensor.get_data()
    assert data["sensor_id"] == "temp_01"
    assert data["room"] == "Living Room"
    assert data["value"] == value


def test_motion_sensor():
    """Test the Motion Sensor functionality."""
    motion = MotionSensor("motion_01", "Hallway")

    value = motion.read_value()
    assert value in ["detected", "none"], "Motion value must be 'detected' or 'none'."

    data = motion.get_data()
    assert data["sensor_id"] == "motion_01"
    assert data["room"] == "Hallway"
    assert data["value"] == value


def test_humidity_sensor():
    """Test the Humidity Sensor functionality."""
    env = EnvironmentManager()
    sensor = HumiditySensor("humidity_01", "Bathroom", env)

    value = sensor.read_value()
    assert isinstance(value, float), "Humidity should be a float."
    assert 0 <= value <= 100, "Humidity should be between 0 and 100."

    data = sensor.get_data()
    assert data["sensor_id"] == "humidity_01"
    assert data["room"] == "Bathroom"
    assert data["value"] == value


def test_gas_sensor():
    """Test the Gas Sensor functionality with numeric value."""
    sensor = GasSensor("gas_01", "Kitchen")

    value = sensor.read_value()

    assert isinstance(value, float), "Gas sensor value should be a float."

    assert 100.0 <= value <= 500.0, "Gas sensor reading out of expected range."

def test_noise_sensor():
    """Test the Noise Sensor functionality."""
    sensor = NoiseSensor("noise_01", "Living Room")

    value = sensor.read_value()
    assert isinstance(value, float), "Noise level should be a float."
    assert 30.0 <= value <= 90.0, "Noise level should be within 30-90 dB."

    data = sensor.get_data()
    assert data["sensor_id"] == "noise_01"
    assert data["room"] == "Living Room"
    assert data["value"] == value
