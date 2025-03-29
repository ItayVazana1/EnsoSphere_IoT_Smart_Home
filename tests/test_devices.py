from devices.lights import Lights
from devices.blinds import Blinds
from devices.air_conditioner import AirConditioner
from devices.robot_vacuum import RobotVacuum
from devices.pet_feeder import PetFeeder
from devices.door_lock import DoorLock
from devices.ventilation_fan import VentilationFan
from devices.window import Window
from devices.security_system import SecuritySystem


# === LIGHTS ===
class DummyMQTT:
    def subscribe(self, *args): pass
    def message_callback_add(self, *args): pass


mqtt_stub = DummyMQTT()

def test_lights_basic_logic():
    lights = Lights("lights_01", "Living Room", mqtt_stub)
    lights.turn_on()
    assert lights.state == "on"
    lights.turn_off()
    assert lights.state == "off"

# === BLINDS ===
def test_blinds_basic_logic():
    blinds = Blinds("blinds_01", "Bedroom", mqtt_stub)
    blinds.open()
    assert blinds.state == "open"
    blinds.close()
    assert blinds.state == "closed"

# === AIR CONDITIONER ===
def test_air_conditioner_basic_logic():
    ac = AirConditioner("ac_01", "Office", mqtt_stub)
    ac.turn_on()
    assert ac.state == "on"
    ac.set_temperature(20.0)
    assert ac.target_temperature == 20.0
    ac.turn_off()
    assert ac.state == "off"

# === ROBOT VACUUM ===
def test_robot_vacuum_basic_logic():
    robo = RobotVacuum("robo_01", "Hallway", mqtt_stub)
    robo.start_cleaning()
    assert robo.state == "on"
    assert robo.mode == "cleaning"
    robo.stop_cleaning()
    assert robo.mode == "idle"
    robo.go_home()
    assert robo.mode == "charging"
    assert robo.state == "off"

# === PET FEEDER ===
def test_pet_feeder_basic_logic():
    feeder = PetFeeder("feeder_01", "Kitchen", mqtt_stub)
    initial = feeder.dispense_count
    feeder.dispense_food()
    assert feeder.dispense_count == initial + 1
    assert feeder.state == "ready"

# === DOOR LOCK ===
def test_door_lock_basic_logic():
    lock = DoorLock("lock_01", "Entrance", mqtt_stub)
    assert lock.state == "locked"
    lock.unlock()
    assert lock.state == "unlocked"
    lock.lock()
    assert lock.locked


# === Ventilation Fan ===
def test_ventilation_fan():
    """Test the Ventilation Fan functionality."""
    fan = VentilationFan("fan_01", "Bathroom", mqtt_client=None)

    fan.receive_command("turn_on")
    assert fan.state == "on", "Fan should be ON after turn_on command."

    fan.receive_command("turn_off")
    assert fan.state == "off", "Fan should be OFF after turn_off command."



# === Window  ===
def test_window():
    """Test the Window device functionality."""
    window = Window("window_01", "Bedroom", mqtt_client=None)

    window.receive_command("open")
    assert window.state == "open", "Window should be open."

    window.receive_command("close")
    assert window.state == "closed", "Window should be closed."



# === Security System ===
def test_security_system():
    """Test Security System functionality."""
    system = SecuritySystem("sec_01", "Entrance", mqtt_client=None)

    system.receive_command("arm")
    assert system.state == "armed"

    system.receive_command("alert")
    assert system.state == "alert"

    system.receive_command("disarm")
    assert system.state == "disarmed"
