import pytest
import time
from core import mqtt_client as mqtt_module
from devices.lights import Lights
from devices.blinds import Blinds
from devices.air_conditioner import AirConditioner
from devices.robot_vacuum import RobotVacuum
from devices.pet_feeder import PetFeeder
from devices.door_lock import DoorLock


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


def test_lights(mqtt_client):
    lights = Lights("lights_01", "Living Room", mqtt_client)
    lights.receive_command("turn_on")
    assert lights.state == "on"
    lights.receive_command("turn_off")
    assert lights.state == "off"


def test_blinds(mqtt_client):
    blinds = Blinds("blinds_01", "Bedroom", mqtt_client)
    blinds.receive_command("open")
    assert blinds.state == "open"
    blinds.receive_command("close")
    assert blinds.state == "closed"


def test_air_conditioner(mqtt_client):
    ac = AirConditioner("ac_01", "Living Room", mqtt_client)
    ac.receive_command("turn_on")
    assert ac.state == "on"
    ac.receive_command("set_temperature", {"temperature": 22})
    assert ac.target_temperature == 22
    ac.receive_command("turn_off")
    assert ac.state == "off"


def test_robot_vacuum(mqtt_client):
    robot = RobotVacuum("vacuum_01", "Entire Home", mqtt_client)
    robot.receive_command("start_cleaning")
    assert robot.state == "on"
    assert robot.mode == "cleaning"
    robot.receive_command("stop_cleaning")
    assert robot.mode == "idle"
    robot.receive_command("go_home")
    assert robot.state == "off"
    assert robot.mode == "charging"


def test_pet_feeder(mqtt_client):
    feeder = PetFeeder("feeder_01", "Kitchen", mqtt_client)
    initial_count = feeder.dispense_count
    feeder.receive_command("dispense_food")
    assert feeder.state == "ready"
    assert feeder.dispense_count == initial_count + 1


def test_door_lock(mqtt_client):
    lock = DoorLock("lock_01", "Entrance", mqtt_client)
    assert lock.state == "locked"
    lock.receive_command("unlock")
    assert lock.state == "unlocked"
    lock.receive_command("lock")
    assert lock.state == "locked"
