"""
Module: corelogic/rule_engine.py
Purpose: Evaluates loaded rules per tick based on current sensor values.
Author: Itay Vazana
"""

from typing import List, Dict, Any


class RuleEngine:
    def __init__(self, rules_by_device: Dict[str, List[Dict[str, Any]]]):
        """
        Initializes RuleEngine with pre-loaded rules organized by device_id.
        """
        self.rules_by_device = rules_by_device

    def evaluate_rules(self, sensors: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evaluates all rules from all devices using current sensor values.

        Returns:
            List of triggered rules with metadata and actions.
        """
        activated_rules = []

        for device_id, rules in self.rules_by_device.items():
            for rule in rules:
                conditions = rule.get("sensor_conditions", [])
                if self.evaluate_conditions(conditions, sensors):
                    activated_rules.append({
                        "rule_id": rule["rule_id"],
                        "triggered": True,
                        "conditions": conditions,
                        "actions": rule["actions"]
                    })

        return activated_rules

    def evaluate_conditions(self, conditions: List[Dict[str, Any]], sensors: Dict[str, Any]) -> bool:
        """
        Evaluates top-level conditions (AND logic). Supports 'any' blocks.
        """
        for cond in conditions:
            if "any" in cond:
                if not self.evaluate_any(cond["any"], sensors):
                    return False
            else:
                if not self.evaluate_single_condition(cond, sensors):
                    return False
        return True

    def evaluate_any(self, condition_list: List[Dict[str, Any]], sensors: Dict[str, Any]) -> bool:
        """
        Evaluates an 'any' condition block.
        """
        for cond in condition_list:
            if self.evaluate_single_condition(cond, sensors):
                return True
        return False

    def evaluate_single_condition(self, cond: Dict[str, Any], sensors: Dict[str, Any]) -> bool:
        """
        Evaluates a single sensor condition.
        """
        sensor_id = cond.get("sensor_id")
        sensor_value = sensors.get(sensor_id)

        if "equals" in cond:
            return sensor_value == cond["equals"]

        if "greater_than" in cond:
            return isinstance(sensor_value, (int, float)) and sensor_value > cond["greater_than"]

        if "less_than" in cond:
            return isinstance(sensor_value, (int, float)) and sensor_value < cond["less_than"]

        if "in_range" in cond:
            low, high = cond["in_range"]
            return isinstance(sensor_value, (int, float)) and low <= sensor_value <= high

        if "in" in cond:
            return sensor_value in cond["in"]

        print(f"[RuleEngine] ❌ Unsupported condition: {cond}")
        return False
