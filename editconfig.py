import ast
import os
import sys
from pathlib import Path
from config import CONFIG



def print_config(config, prefix=""):
    """Print every config value on its own line."""
    for key, value in config.items():
        full_key = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict):
            print_config(value, full_key)
        else:
            print(f"{full_key}: {value}")


def get_nested(config, key_path):
    """Return the dictionary containing the final key and the key name."""
    parts = key_path.split(".")
    current = config

    for part in parts[:-1]:
        if part not in current or not isinstance(current[part], dict):
            return None, None
        current = current[part]

    return current, parts[-1]


def edit_config(config=None, path=None):
    if config is None:
        config = CONFIG
    if path is None:
        path = Path(__file__).parent / "config.py"

    config = dict(config)

    print("Type a setting name to change, or 'done' to save and exit.\n")
    print("Current configuration:\n")
    print_config(config)
    print()

    while True:
        key = input("Setting name: ").strip()

        if key.lower() in {"done", "quit", "exit"}:
            break

        parent, final_key = get_nested(config, key)

        if parent is None or final_key not in parent:
            print("Unknown setting.\n")
            continue

        print(f"Current value: {parent[final_key]}")
        value = input(f"New value for {key}: ").strip()

        try:
            parsed = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            parsed = value

        parent[final_key] = parsed

        print(f"\nUpdated {key} = {parsed}\n")

    target = Path(path)
    target.write_text(
        "CONFIG = " + repr(config) + "\n",
        encoding="utf-8",
    )

    return config


if __name__ == "__main__":
    edit_config()

