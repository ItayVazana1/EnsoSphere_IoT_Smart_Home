import json
import os
from jsonschema import validate, ValidationError
from datetime import datetime
from core import mqtt_client as mqtt_module

# Resolve dynamic base directory
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# RULES_PATH = os.path.join(base_dir, "rules", "rules_example.json")
RULES_PATH = os.path.join(base_dir, "rules", "official_rules.json")
SCHEMA_PATH = os.path.join(base_dir, "rules", "rule_schema.json")

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
        # print(f"⚠️ Missing value for condition: {condition}")
        return False

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
        # print(f"⚠️ Error evaluating condition: {e}")
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
    logic = rule.get("conditions_logic", "AND")
    conditions = rule.get("conditions", [])
    results = [evaluate_condition(cond, env_data, sensor_data) for cond in conditions]

    if logic == "AND":
        return all(results)
    elif logic == "OR":
        return any(results)
    else:
        print(f"⚠️ Unknown logic type in rule {rule['id']}: {logic}")
        return False

def process_all_rules(rules, env_data, sensor_data, mqtt_client):
    """
    Evaluate all rules and trigger their actions if conditions are met.
    Returns:
        triggered (list): IDs of rules that were triggered.
        not_triggered (list): IDs of rules that were not triggered.
    """
    triggered = []
    not_triggered = []

    for rule in rules:
        rule_id = rule["id"]
        if evaluate_rule(rule, env_data, sensor_data):
            triggered.append(rule_id)
            for action in rule["actions"]:
                execute_action(action, mqtt_client)
        else:
            not_triggered.append(rule_id)

    return triggered, not_triggered


def execute_action(action, mqtt_client):
    device_id = action["device_id"]
    command = action["command"]
    parameters = action.get("parameters", {})

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

if __name__ == "__main__":
    main()

    mqtt = mqtt_module.create_mqtt_client()
    mqtt.loop_start()

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