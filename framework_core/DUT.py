import os
import sys
from typing import Dict, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.alias import *
from framework_core.SOC import SOC
from drivers.relay_controller import USBRelayController

class DUT:
    def __init__(self, name: str, data: Dict):
        self.name = name
        # self.raw_data = data

        self.soc_objects = {}
        socs = data.get(SOC_ALIAS, {})
        self._safe_create_soc_object(socs=socs)

    def _safe_create_soc_object(self, socs: dict):
        """
            Note: avoid using commong config as dict in dut section
            eg:
            - good practice:
                "device_under_test": {
                    "hi": "###$$%%",
                    "raspberry_pi3": {
                    }
                }
            - bad practice:
                "device_under_test": {
                    "hi": {
                        "config_1": "###$$%%"
                    },
                    "raspberry_pi3": {
                    }
                }
        """
        for soc_name, soc_data in socs.items():
            if isinstance(soc_data, dict):
                self.soc_objects[soc_name] = SOC(name=soc_name, data=soc_data)

    def init_resources(self):
        # init dut in here

        # init soc
        for soc_name, soc_object in self.soc_objects.items():
            soc_object.init_resources()

    def _init_usb_relay(self):
        self.power_control = USBRelayController(relay_name=self.power.device)


    # def __repr__(self):
    #     # TODO: create logger in here and put it into debug log
    #     print(f"__repr__ of SoC: {self.name}")
    #     return str(self.__dict__)