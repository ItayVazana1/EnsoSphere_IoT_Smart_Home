import json
import os
from jsonschema import validate, ValidationError
from datetime import datetime
from core import mqtt_client as mqtt_module


RULES_PATH = "../rules/rules_example.json"
SCHEMA_PATH = "../rules/rule_schema.json"



def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def validate_rules(rules, schema):
    for rule in rules:
        try:
            validate(instance=rule, schema=schema)
        except ValidationError as e:
            print(f"[SCHEMA ERROR] Rule ID {rule.get('id', 'UNKNOWN')} failed validation:")
            print(e.message)
            return False
    return True



def evaluate_condition(condition, env_data, sensor_data):
    """
    Evaluate a single condition against current sensor or environment data.

    Parameters:
        condition (dict): One condition from the rule.
        env_data (dict): Environment state (e.g., temperature, is_daytime).
        sensor_data (dict): Dictionary of latest sensor values keyed by sensor_id.

    Returns:
        bool: True if condition is met, False otherwise.
    """
    operator = condition["operator"]
    expected = condition["value"]

    if condition["type"] == "environment":
        key = condition["parameter"]
        actual = env_data.get(key)

    elif condition["type"] == "sensor":
        sensor_id = condition["sensor_id"]
        actual = sensor_data.get(sensor_id)

    else:
        print(f"❌ Unknown condition type: {condition['type']}")
        return False

    if actual is None:
        print(f"⚠️ Missing value for condition: {condition}")
        return False

    # Compare actual vs expected using operator
    try:
        if operator == "==":
            return actual == expected
        elif operator == "!=":
            return actual != expected
        elif operator == ">":
            return actual > expected
        elif operator == "<":
            return actual < expected
        elif operator == ">=":
            return actual >= expected
        elif operator == "<=":
            return actual <= expected
        else:
            print(f"❌ Unsupported operator: {operator}")
            return False
    except Exception as e:
        print(f"⚠️ Error evaluating condition: {e}")
        return False



def display_rules(rules):
    print(f"\n📜 Loaded {len(rules)} rule(s):")
    for rule in rules:
        print(f"\n🆔 Rule ID: {rule['id']}")
        print(f"🔖 Description: {rule['description']}")
        print(f"📚 Conditions ({rule['conditions_logic']}):")
        for cond in rule["conditions"]:
            if cond["type"] == "sensor":
                print(f"  - [Sensor] {cond['sensor_id']} {cond['operator']} {cond['value']}")
            elif cond["type"] == "environment":
                print(f"  - [Env] {cond['parameter']} {cond['operator']} {cond['value']}")
        print("🎯 Actions:")
        for action in rule["actions"]:
            print(f"  - Send '{action['command']}' to {action['device_id']}")



def evaluate_rule(rule, env_data, sensor_data):
    """
    Evaluate all conditions in a rule based on the current environment and sensor data.

    Parameters:
        rule (dict): A single rule object from the rules list.
        env_data (dict): Dictionary of current environment data.
        sensor_data (dict): Dictionary of current sensor values.

    Returns:
        bool: True if the rule conditions are satisfied based on the logic ('AND' / 'OR').
    """
    logic = rule.get("conditions_logic", "AND")
    conditions = rule.get("conditions", [])

    results = []
    for cond in conditions:
        result = evaluate_condition(cond, env_data, sensor_data)
        results.append(result)

    if logic == "AND":
        return all(results)
    elif logic == "OR":
        return any(results)
    else:
        print(f"⚠️ Unknown logic type in rule {rule['id']}: {logic}")
        return False


def process_all_rules(rules, env_data, sensor_data, mqtt_client):
    """
    Process all rules: evaluate each rule's conditions, and execute actions if met.

    Parameters:
        rules (list): List of validated rules.
        env_data (dict): Current environment state.
        sensor_data (dict): Latest values from all sensors.
        mqtt_client (paho.mqtt.client.Client): Connected MQTT client for publishing.
    """
    for rule in rules:
        rule_id = rule["id"]
        if evaluate_rule(rule, env_data, sensor_data):
            print(f"\n✅ Rule '{rule_id}' triggered!")
            for action in rule["actions"]:
                execute_action(action, mqtt_client)
        else:
            print(f"\n⏸ Rule '{rule_id}' conditions not met.")




def execute_action(action, mqtt_client):
    """
    Publish an action command to the appropriate MQTT topic.

    Parameters:
        action (dict): Action from rule (must include device_id, command, parameters).
        mqtt_client (paho.mqtt.client.Client): Connected MQTT client instance.
    """
    device_id = action["device_id"]
    command = action["command"]
    parameters = action.get("parameters", {})

    # נניח פורמט של device_id: <device_type>_<room>
    try:
        device_type, room = device_id.split("_", 1)
    except ValueError:
        print(f"❌ Invalid device_id format: {device_id}")
        return

    topic = f"MyHome/{room}/{device_type}/{device_id}"

    payload = {
        "device_id": device_id,
        "command": command,
        "parameters": parameters,
        "timestamp": datetime.now().isoformat()
    }

    payload_str = json.dumps(payload)
    mqtt_client.publish(topic, payload_str)
    print(f"📡 Published to {topic} → {payload_str}")



# --- Main ---
def main():
    rules_data = load_json(RULES_PATH)
    schema = load_json(SCHEMA_PATH)

    rules = rules_data["rules"]

    print("🔍 Validating rules...")
    if not validate_rules(rules, schema):
        print("❌ One or more rules are invalid.")
        return

    print("✅ Rules validated successfully.")
    display_rules(rules)


# ...

if __name__ == "__main__":
    main()

    # Create MQTT client
    mqtt = mqtt_module.create_mqtt_client()
    mqtt.loop_start()

    # Sample data
    env_data = {
        "temperature": 29,
        "is_daytime": True
    }

    sensor_data = {}

    rules_data = load_json(RULES_PATH)
    rules = rules_data["rules"]

    process_all_rules(rules, env_data, sensor_data, mqtt)

    mqtt.loop_stop()
    mqtt.disconnect()


