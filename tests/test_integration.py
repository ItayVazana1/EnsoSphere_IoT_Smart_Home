from core.mqtt_client import create_mqtt_client
from core.environment_manager import EnvironmentManager
from sensors.motion_sensor import MotionSensor
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.gas_sensor import GasSensor
from sensors.noise_sensor import NoiseSensor
from devices.lights import Lights
from devices.blinds import Blinds
from devices.air_conditioner import AirConditioner
from devices.robot_vacuum import RobotVacuum
from devices.pet_feeder import PetFeeder
from devices.door_lock import DoorLock
import time
import yaml

def load_config():
    with open("../config.yaml", "r") as file:
        return yaml.safe_load(file)

def test_all_components():
    config = load_config()
    env = EnvironmentManager()
    mqtt_client = create_mqtt_client()
    mqtt_client.loop_start()

    time.sleep(1)

    print("\n=== TESTING SENSORS ===")
    sensor_classes = {
        "Motion": lambda i, r: MotionSensor(i, r, mqtt_client=mqtt_client),
        "Temperature": lambda i, r: TemperatureSensor(i, r, mqtt_client=mqtt_client, env_manager=env),
        "Humidity": lambda i, r: HumiditySensor(i, r, mqtt_client=mqtt_client, env_manager=env),
        "Gas": lambda i, r: GasSensor(i, r, mqtt_client=mqtt_client, env_manager=env),
        "Noise": lambda i, r: NoiseSensor(i, r, mqtt_client=mqtt_client, env_manager=env)
    }

    for room in config['rooms']:
        for sensor_name in room.get("sensors", []):
            sensor_class = sensor_classes.get(sensor_name)
            if sensor_class:
                sensor_id = f"{sensor_name.lower()}_{room['name'].replace(' ', '_')}"
                sensor = sensor_class(sensor_id, room['name'])
                value = sensor.read_value()
                print(f"[Sensor] {sensor_id} → {value}")

    print("\n=== TESTING DEVICES ===")
    device_classes = {
        "Lights": Lights,
        "Blinds": Blinds,
        "Air Conditioner": AirConditioner,
        "Robot Vacuum": RobotVacuum,
        "Pet Feeder": PetFeeder,
        "Door Lock": DoorLock
    }

    test_commands = {
        "Lights": "turn_on",
        "Blinds": "open",
        "Air Conditioner": "turn_on",
        "Robot Vacuum": "start_cleaning",
        "Pet Feeder": "dispense_food",
        "Door Lock": "unlock"
    }

    for room in config['rooms']:
        for device_name in room.get("devices", {}).get("actuators", []):
            device_class = device_classes.get(device_name)
            if device_class:
                device_id = f"{device_name.lower().replace(' ', '_')}_{room['name'].replace(' ', '_')}"
                device = device_class(device_id, room['name'], mqtt_client)
                command = test_commands[device_name]
                print(f"[Device] Sending '{command}' → {device_id}")
                device.receive_command(command)
                status = device.get_status()
                print(f"[Status] {status}")

    mqtt_client.loop_stop()
    mqtt_client.disconnect()
