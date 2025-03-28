from devices.lights import Lights
from devices.blinds import Blinds
from devices.air_conditioner import AirConditioner
from devices.robot_vacuum import RobotVacuum
from devices.pet_feeder import PetFeeder
from devices.door_lock import DoorLock


def test_lights():
    """Test the Lights device functionality."""
    lights = Lights("lights_01", "Living Room")

    # Test turning the lights on
    lights.receive_command("turn_on")
    assert lights.state == "on", "Lights failed to turn on."

    # Test turning the lights off
    lights.receive_command("turn_off")
    assert lights.state == "off", "Lights failed to turn off."


def test_blinds():
    """Test the Blinds device functionality."""
    blinds = Blinds("blinds_01", "Bedroom")

    # Test opening the blinds
    blinds.receive_command("open")
    assert blinds.state == "open", "Blinds failed to open."

    # Test closing the blinds
    blinds.receive_command("close")
    assert blinds.state == "closed", "Blinds failed to close."


def test_air_conditioner():
    """Test the Air Conditioner device functionality."""
    ac = AirConditioner("ac_01", "Living Room")

    # Test turning the AC on
    ac.receive_command("turn_on")
    assert ac.state == "on", "Air Conditioner failed to turn on."

    # Test setting temperature
    ac.receive_command("set_temperature", {"temperature": 22})
    assert ac.target_temperature == 22, "Air Conditioner failed to set temperature."

    # Test turning the AC off
    ac.receive_command("turn_off")
    assert ac.state == "off", "Air Conditioner failed to turn off."


def test_robot_vacuum():
    """Test the Robot Vacuum device functionality."""
    robot = RobotVacuum("vacuum_01", "Entire Home")

    # Start cleaning
    robot.receive_command("start_cleaning")
    assert robot.state == "on", "Robot should be on after cleaning starts."
    assert robot.mode == "cleaning", "Robot should be in cleaning mode."

    # Stop cleaning
    robot.receive_command("stop_cleaning")
    assert robot.mode == "idle", "Robot should be idle after stopping."

    # Go to charging station
    robot.receive_command("go_home")
    assert robot.state == "off", "Robot should be off when going home."
    assert robot.mode == "charging", "Robot should be charging."


def test_pet_feeder():
    """Test the Pet Feeder device functionality."""
    feeder = PetFeeder("feeder_01", "Kitchen")

    assert feeder.state == "ready"
    assert feeder.dispense_count == 0

    # Dispense food
    feeder.receive_command("dispense_food")
    assert feeder.state == "ready", "Feeder should return to ready state after dispensing."
    assert feeder.dispense_count == 1, "Dispense count should increment after dispensing."


def test_door_lock():
    """Test the Door Lock device functionality."""
    lock = DoorLock("lock_01", "Entrance")

    # Initial state should be locked
    assert lock.state == "locked", "Initial state should be locked."

    # Unlock the door
    lock.receive_command("unlock")
    assert lock.state == "unlocked", "Door should be unlocked."

    # Lock the door again
    lock.receive_command("lock")
    assert lock.state == "locked", "Door should be locked."
