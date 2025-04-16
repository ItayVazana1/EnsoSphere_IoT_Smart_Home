"""
Module: corelogic/rules_loader.py
Purpose: Loads all device-specific rule JSON files into a unified dictionary for rule evaluation.
Author: Itay Vazana
"""

import os
import json

RULES_DIR = os.path.join(os.path.dirname(__file__), "rules")


def load_all_rules():
    """
    Loads all rules from JSON files in the rules/ directory.

    Returns:
        dict: A dictionary mapping device_id → list of rule dicts.
              Example: { "lights_kitchen": [ {...}, {...} ], ... }
    """
    all_rules = {}

    if not os.path.exists(RULES_DIR):
        print(f"[Rules Loader] ❌ Rules directory not found: {RULES_DIR}")
        return all_rules

    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(RULES_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    rules = json.load(f)

                if not isinstance(rules, list):
                    raise ValueError("Rule file must contain a list of rules")

                for rule in rules:
                    device_id = None
                    for action in rule.get("actions", []):
                        device_id = action.get("device_id")
                        break  # assume all actions in rule target same device

                    if not device_id:
                        print(f"[Rules Loader] ⚠️ Rule missing device in actions: {rule.get('rule_id')}")
                        continue

                    all_rules.setdefault(device_id, []).append(rule)

                print(f"[Rules Loader] ✅ Loaded {len(rules)} rule(s) from {filename}")

            except Exception as e:
                print(f"[Rules Loader] ⚠️ Failed to load {filename}: {e}")

    return all_rules
