import json
import yaml
import os
import sys
import copy
from typing import Dict, List, Optional
from utils.alias import *
# test in local file
# from alias import *

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework_core.SUT import SUT


class AttrDict:
    def __init__(self, data):
        """
            attribute class with recursion
            eg:
                data = "network": {'interface': 'end1', 'ip': '10.0.0.3', 'MAC': 'ee:2f:2f:c8:94:74'}
                ->
                AttrDict(data) ~ AttrDict.network = {'interface': 'end1', 'ip': '10.0.0.3', 'MAC': 'ee:2f:2f:c8:94:74'}
                then
                ->
                AttrDict(data=interface) ~ AttrDict.interface = 'end1'
                -> loop to the end pair of "network"
        """
        for k, v in data.items():
            if isinstance(v, dict):
                v = AttrDict(v)
            setattr(self, k, v)

    def __repr__(self):
        return str(self.__dict__)

def json_safe_get(data: Dict, keys: List[str], default=None) -> Optional[Dict]:
    current_data = data
    for key in keys:
        if isinstance(current_data, dict):
            current_data = current_data.get(key)
            if current_data is None:
                return default
        else:
            return default
    return current_data if current_data is not None else default

class ConfigLoader:
    def __init__(self, path: str):
        self.config: dict = self._load_config(path)
        self.system_kits: dict[SUT] = self._parse_system_kits()
        self.SoC_block: dict = {}
        self.device_under_test_block: dict = {}
        self.system_under_test_block: dict = {}
        # fill attr field base on field in config file
        self._init_resources()

    def _load_config(self, path: str) -> Dict:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path, 'r') as f:
            if path.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
            elif path.endswith('.json'):
                return json.load(f)
            else:
                raise ValueError("Unsupported file format")

    def _parse_system_kits(self) -> Dict[str, SUT]:

        parsed_kits: dict = {}
        self.system_under_test_block: dict = self.config.get(SUT_ALIAS, {})

        self.device_under_test_block: dict = self.config.get(DUT_ALIAS, {})
        self.SoC_block: dict = self.config.get(SOC_ALIAS, {})

        filtered_config = self.filter_system_config().get(SUT_ALIAS, {})

        unregister_config = self.filter_unregister_system_config().get(SUT_ALIAS, {})

        for sut_name, sut_data in self.system_under_test_block.items():
            # create object with filtered exist data field of duts and socs
            filtered_sut_config = filtered_config[sut_name]
            unregister_sut_config = unregister_config[sut_name]
            sut_obj = SUT(name=sut_name, data=filtered_sut_config)

            # add config field as attr for SUT
            # Working as shallow copy as reference so don't need use deep copy and return value
            # ConfigLoader.add_config_as_atrr(data=unregister_sut_config, ignore_list=[f"{DUT_ALIAS}"], obj=sut_obj)
            ConfigLoader.add_config_as_attr_recursion(data=unregister_sut_config, ignore_list=[f"{DUT_ALIAS}"], obj=sut_obj)

            # add config field as attr for DUT
            for dut_name, dut_object in sut_obj.dut_objects.items():
                dut_data = sut_data.get(DUT_ALIAS, {}).get(dut_name, {})
                # dut info get from dut data block
                get_dut_data = self.device_under_test_block.get(dut_name, {})
                # dut info get from sut data block
                unregister_dut_config = unregister_sut_config.get(DUT_ALIAS, {})
                ConfigLoader.deep_merge_dicts(get_dut_data, unregister_dut_config)
                # ConfigLoader.add_config_as_atrr(data=get_dut_data, ignore_list=[f"{dut_name}"], obj=dut_object)
                ConfigLoader.add_config_as_attr_recursion(data=get_dut_data, ignore_list=[f"{dut_name}"], obj=dut_object)

                # add config field as attr for SoC
                for soc_name, soc_object in dut_object.soc_objects.items():
                    soc_data = dut_data.get(SOC_ALIAS, {})
                    get_soc_data = self.SoC_block.get(soc_name, {})
                    # soc info get from sut data block
                    unregister_soc_config = unregister_dut_config.get(dut_name, {}).get(SOC_ALIAS, {})
                    get_soc_data_in_sut = soc_data.get(soc_name, {})

                    ConfigLoader.deep_merge_dicts(get_soc_data_in_sut, unregister_soc_config)
                    ConfigLoader.deep_merge_dicts(get_soc_data_in_sut, get_soc_data)
                    # ConfigLoader.add_config_as_atrr(data=get_soc_data_in_sut, ignore_list=[f""], obj=soc_object)
                    ConfigLoader.add_config_as_attr_recursion(data=get_soc_data_in_sut, ignore_list=[f""], obj=soc_object)


            parsed_kits[sut_name] = sut_obj

        # test in local file
        # print("--------------------------------------------")
        # print((parsed_kits))
        # print("--------------------------------------------")
        # print(vars(parsed_kits['system_2']))
        # print("--------------------------------------------")
        # print(vars(parsed_kits['system_2'].dut_objects['raspberry_pi3']))
        # print("--------------------------------------------")
        # print(vars(parsed_kits['system_2'].dut_objects['raspberry_pi3'].soc_objects['BCM2837']))
        # print("--------------------------------------------")
        # print((parsed_kits['system_2'].dut_objects['raspberry_pi3'].soc_objects['BCM2837'].network))
        # print("--------------------------------------------")

        return parsed_kits
    
    @staticmethod
    def add_config_as_atrr(data: dict, ignore_list: list, obj: object):
        for ele_name, ele_data in data.items():
            if (ele_name in ignore_list):
                # do not add device under test as attr of class
                pass
            else:
                # check object has attribute
                if not (hasattr(obj, ele_name)):
                    setattr(obj, ele_name, ele_data)

    @staticmethod
    def add_config_as_attr_recursion(data: dict, ignore_list: list, obj: object):
        for key, value in data.items():
            if key in ignore_list:
                continue

            if isinstance(value, dict):
                # Nếu object chưa có attribute này, khởi tạo bằng AttrDict
                if not hasattr(obj, key):
                    nested_obj = AttrDict({})
                    setattr(obj, key, nested_obj)
                else:
                    nested_obj = getattr(obj, key)

                # recursion into sub dict
                ConfigLoader.add_config_as_attr_recursion(value, ignore_list, nested_obj)
            else:
                if not hasattr(obj, key):
                    setattr(obj, key, value)

    @staticmethod
    def deep_merge_dicts(base, override):
        for k, v in override.items():
            if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                ConfigLoader.deep_merge_dicts(base[k], v)
            else:
                base[k] = v
        return base
    
    def filter_system_config(self) -> dict:
        """
        Return a new config dict with only valid device_under_test and SoC entries
        without modifying the original input.
        """
        filtered_config = {
            f"{SUT_ALIAS}": {}
        }
    
        for system_name, system_data in self.system_under_test_block.items():
            dut_dict = system_data.get(DUT_ALIAS, {})
            new_dut_dict = {}
    
            for dut_name, dut_data in dut_dict.items():
                if dut_name not in self.device_under_test_block:
                    continue  # Skip invalid DUT
                
                new_dut_data = copy.deepcopy(dut_data)
                soc_block = new_dut_data.get(SOC_ALIAS, {})
                new_soc_block = {}
    
                for soc_name, soc_data in soc_block.items():
                    if soc_name in self.SoC_block:
                        new_soc_block[soc_name] = copy.deepcopy(soc_data)
    
                if new_soc_block:
                    new_dut_data[SOC_ALIAS] = new_soc_block
                    new_dut_dict[dut_name] = new_dut_data
    
            if new_dut_dict:
                new_system_data = {
                    **{k: copy.deepcopy(v) for k, v in system_data.items() if k != DUT_ALIAS},
                    DUT_ALIAS: new_dut_dict
                }
                filtered_config[f"{SUT_ALIAS}"][system_name] = new_system_data
    
        return filtered_config

    def filter_unregister_system_config(self) -> dict:
        """
            return dict contain unregister config field
        """
        invalid_config = {
            f"{SUT_ALIAS}": {}
        }

        for system_name, system_data in self.system_under_test_block.items():
            dut_dict = system_data.get(DUT_ALIAS, {})
            invalid_dut_dict = {}

            for dut_name, dut_data in dut_dict.items():
                # Nếu DUT không hợp lệ, giữ nguyên toàn bộ
                if dut_name not in self.device_under_test_block:
                    invalid_dut_dict[dut_name] = copy.deepcopy(dut_data)
                    continue

                # DUT hợp lệ, nhưng cần kiểm tra SoC
                new_invalid_soc_block = {}
                soc_block = dut_data.get(SOC_ALIAS, {})

                for soc_name, soc_data in soc_block.items():
                    if soc_name not in self.SoC_block:
                        new_invalid_soc_block[soc_name] = copy.deepcopy(soc_data)

                if new_invalid_soc_block:
                    new_dut_data = {
                        **{k: copy.deepcopy(v) for k, v in dut_data.items() if k != SOC_ALIAS},
                        SOC_ALIAS: new_invalid_soc_block
                    }
                    invalid_dut_dict[dut_name] = new_dut_data

            if invalid_dut_dict:
                new_system_data = {
                    **{k: copy.deepcopy(v) for k, v in system_data.items() if k != DUT_ALIAS},
                    DUT_ALIAS: invalid_dut_dict
                }
                invalid_config[f"{SUT_ALIAS}"][system_name] = new_system_data

        return invalid_config
    
    def _init_resources(self):
        for sut_name, sut_object in self.system_kits.items():
            sut_object.init_resources()

    def get_sut(self, name: str) -> Optional[SUT]:
        return self.system_kits.get(name)

    def get_system_kits(self) -> dict[SUT]:
        return self.system_kits
    

# test in local file
# loader = ConfigLoader("/home/yzungx/ws/automation_fw/automation_framework/config/pi3_config.json")
# sut = loader.get_sut("system_2")
# suts = loader.get_system_kits()