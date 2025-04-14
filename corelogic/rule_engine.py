"""
Module: corelogic/rule_engine.py
Purpose: Loads and evaluates rules per tick based on sensor values
Author: Itay Vazana
"""

import os
import json
from typing import List, Dict, Any

RULES_DIR = os.path.join(os.path.dirname(__file__), "../rules")


class RuleEngine:
    def __init__(self):
        """
        Initializes the RuleEngine by loading all rule files from the rules/ directory.
        """
        self.rules: List[Dict[str, Any]] = []
        self.load_all_rules()

    def load_all_rules(self):
        """
        Loads all rule JSON files from the rules directory.
        """
        for filename in os.listdir(RULES_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(RULES_DIR, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    try:
                        rules = json.load(file)
                        self.rules.extend(rules)
                    except json.JSONDecodeError as e:
                        print(f"Failed to load {filename}: {e}")

    def evaluate_rules(self, sensors: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evaluates all rules against the provided sensor values.

        Args:
            sensors (dict): Sensor values from the current tick.

        Returns:
            List[dict]: List of activated rules with their actions and metadata.
        """
        activated_rules = []

        for rule in self.rules:
            if self.evaluate_conditions(rule.get("sensor_conditions", []), sensors):
                activated_rules.append({
                    "rule_id": rule["rule_id"],
                    "triggered": True,
                    "conditions": rule["sensor_conditions"],
                    "actions": rule["actions"]
                })

        return activated_rules

    def evaluate_conditions(self, conditions: List[Dict[str, Any]], sensors: Dict[str, Any]) -> bool:
        """
        Evaluates all conditions for a single rule. Returns True if all are satisfied.

        Args:
            conditions (List[dict]): List of sensor-based conditions.
            sensors (dict): All current sensor values.

        Returns:
            bool: True if all conditions are met.
        """
        for cond in conditions:
            sensor_id = cond.get("sensor_id")
            sensor_value = sensors.get(sensor_id)

            if "equals" in cond:
                if sensor_value != cond["equals"]:
                    return False
            elif "greater_than" in cond:
                if not isinstance(sensor_value, (int, float)) or sensor_value <= cond["greater_than"]:
                    return False
            elif "less_than" in cond:
                if not isinstance(sensor_value, (int, float)) or sensor_value >= cond["less_than"]:
                    return False
            elif "in_range" in cond:
                low, high = cond["in_range"]
                if not isinstance(sensor_value, (int, float)) or not (low <= sensor_value <= high):
                    return False
            elif "in" in cond:
                if sensor_value not in cond["in"]:
                    return False
            else:
                print(f"Unsupported condition in rule: {cond}")
                return False

        return True