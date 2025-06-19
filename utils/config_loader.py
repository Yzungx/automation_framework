import json
import yaml
import sys
import os
from typing import Dict, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework_core.SUT import SUT


def json_safe_get(data: Dict, keys: List[str], default=None):
    """
    Safely retrieves a value from a nested dictionary (JSON-like structure).
    Args:
        data (dict): The dictionary to retrieve the value from.
        keys (list): A list of keys representing the path to the desired value.
        default: The default value to return if any key in the path is not found.
    Returns:
        The retrieved value or the default value if not found.
    eg:
        nested_json_data = '{"user": {"profile": {"email": "test@example.com", "age": 25}}}'
        data = json.loads(nested_json_data)
        email = safe_get(data, ["user", "profile", "email"], "N/A")
        print(f"Email (via safe_get): {email}")
        address = safe_get(data, ["user", "address", "street"], "Unknown Street")
        print(f"Address (via safe_get): {address}")
    """
    current_data = data
    for key in keys:
        if isinstance(current_data, dict):
            current_data = current_data.get(key)
            if current_data is None:
                return default
        else:
            return default  # Not a dictionary, can't continue path
    return current_data if current_data is not None else default

class ConfigLoader:
    def __init__(self, path: str):
        self.config = self.load_config(path)
        self.data = self._parse_config()

    def load_config(self, path: str) -> Dict:
        """
        Load configuration from a YAML or JSON file.
        Args:
            path (str): Path to the configuration file.
        Returns:
            Dict: Loaded configuration data.
        """
        try:
            with open(path, 'r') as f:
                if path.endswith('.yaml') or path.endswith('.yml'):
                    return yaml.safe_load(f)
                elif path.endswith('.json'):
                    return json.load(f)
                else:
                    raise ValueError("Unsupported file format. Use .yaml, .yml, or .json")
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {path}")
        except Exception as e:
            raise Exception(f"Error loading config file: {e}")
        
    def _parse_config(self):
        suts = {}
        system_kit : Dict = json_safe_get(self.config, ["System_kit"])
        suts_name : list = json_safe_get(system_kit, ["suts"])
        # print(system_kit)

        for sut_name in suts_name:
            sut = json_safe_get(system_kit, [f"{sut_name}"])
            sut_obj = SUT(sut=sut)
            suts[sut_name] = sut_obj

            print(suts)

ConfigLoader = ConfigLoader("/home/yzungx/ws/automation_fw/automation_framework/config/pi3_config.json")
# print(ConfigLoader.config)