"""
Module: rule_engine.py
Purpose: Loads and evaluates JSON-based rules for device automation
"""

import os
import json
from datetime import datetime

class RuleEngine:
    def __init__(self, rules_folder):
        self.rules_folder = rules_folder
        self.rules = []

    def load_rules_from_folder(self):
        """
        Loads all JSON rule files from the specified folder into memory.
        """
        for filename in os.listdir(self.rules_folder):
            if filename.endswith(".json"):
                path = os.path.join(self.rules_folder, filename)
                with open(path, 'r', encoding='utf-8') as file:
                    rules = json.load(file)
                    self.rules.extend(rules)
        print(f"📥 Loaded {len(self.rules)} rules from {self.rules_folder}")

    def evaluate_rules(self, state_id, sensor_outputs):
        """
        Evaluates all loaded rules based on the current sensor outputs.

        Args:
            state_id (int): ID of the current tick/state.
            sensor_outputs (dict): Dictionary of all evaluated sensors in current tick.

        Returns:
            list: A list of actions (dicts) to execute.
        """
        triggered = []
        for rule in self.rules:
            if self._evaluate_conditions(rule.get("sensor_conditions", []), sensor_outputs):
                for action in rule.get("actions", []):
                    command = action["command"]

                    # הגנה ← אם זה string, ננסה להמיר ל־dict
                    if isinstance(command, str):
                        try:
                            command = json.loads(command)
                            print(f"[DEBUG] Parsed string command for {action['device_id']}")
                        except json.JSONDecodeError:
                            print(f"[WARNING] Malformed command string for {action['device_id']}: {command}")
                            continue

                    triggered.append({
                        "state_id": state_id,
                        "rule_id": rule["rule_id"],
                        "device_id": action["device_id"],
                        "command": command,
                        "timestamp": datetime.utcnow().isoformat(),
                        "triggered": True,
                        "conditions_json": rule.get("sensor_conditions", []),
                        "actions_json": [action]
                    })
        return triggered



    def _evaluate_conditions(self, conditions, sensor_outputs):
        for condition in conditions:
            if "any" in condition:
                if not any(self._evaluate_conditions([sub], sensor_outputs) for sub in condition["any"]):
                    return False
            elif "sensor_id" in condition:
                sensor_id = condition["sensor_id"]
                value = sensor_outputs.get(sensor_id)
                if value is None:
                    return False

                if "equals" in condition and value != condition["equals"]:
                    return False
                if "in_range" in condition:
                    min_val, max_val = condition["in_range"]
                    if not (min_val <= float(value) <= max_val):
                        return False
                if "less_than" in condition and float(value) >= condition["less_than"]:
                    return False
                if "greater_than" in condition and float(value) <= condition["greater_than"]:
                    return False
                if "in" in condition and value not in condition["in"]:
                    return False
            else:
                return False
        return True
