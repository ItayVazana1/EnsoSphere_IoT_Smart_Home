"""
Module: corelogic/rule_engine.py
Purpose: Evaluate rules against current sensor outputs and return triggered actions.
Author: Itay Vazana
"""

from typing import List, Dict, Any
import json

class RuleEngine:
    def __init__(self, rules: List[Dict[str, Any]]):
        """
        Initialize RuleEngine with list of rule definitions.

        Args:
            rules (list): List of rule dicts as loaded from JSON file.
        """
        self.rules = rules

    def evaluate_rules(self, sensor_outputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evaluate all rules based on current sensor outputs.

        Args:
            sensor_outputs (dict): Dictionary of sensor_id to current value.

        Returns:
            list: List of rule results. Each includes rule_id, triggered, conditions_json, actions_json
        """
        results = []

        for rule in self.rules:
            rule_id = rule["rule_id"]
            conditions = rule.get("sensor_conditions", [])
            actions = rule.get("actions", [])
            triggered = self._check_conditions(conditions, sensor_outputs)

            results.append({
                "rule_id": rule_id,
                "triggered": triggered,
                "conditions_json": json.dumps(conditions),
                "actions_json": json.dumps(actions if triggered else [])
            })

        return results

    def _check_conditions(self, conditions: List[Dict[str, Any]], sensors: Dict[str, Any]) -> bool:
        """
        Check whether all conditions match the current sensor values.

        Args:
            conditions (list): List of sensor condition dicts.
            sensors (dict): Current sensor values.

        Returns:
            bool: True if all conditions are met.
        """
        for cond in conditions:
            sensor_id = cond["sensor_id"]
            expected_value = cond.get("equals")
            lt = cond.get("less_than")
            gt = cond.get("greater_than")

            actual = sensors.get(sensor_id)

            if expected_value is not None and actual != expected_value:
                return False
            if lt is not None and not (isinstance(actual, (int, float)) and actual < lt):
                return False
            if gt is not None and not (isinstance(actual, (int, float)) and actual > gt):
                return False

        return True