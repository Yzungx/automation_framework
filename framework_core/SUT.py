import os
import sys
from typing import Dict, List
from framework_core.DUT import DUT

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.alias import *

class SUT:
    def __init__(self, name: str, data: Dict):
        self.name = name
        # self.raw_data = data
        self.dut_objects = {}

        duts = data.get(DUT_ALIAS, {})
        self._safe_create_dut_object(duts=duts)
    
    def _safe_create_dut_object(self, duts: dict):
        for dut_name, dut_data in duts.items():
            if isinstance(dut_data, dict):
                self.dut_objects[dut_name] = DUT(name=dut_name, data=dut_data)

    def init_resources(self):
        # init sut in here

        # init dut
        for dut_name, dut_object in self.dut_objects.items():
            # print(dut_object)
            dut_object.init_resources()

    # def __repr__(self):
    #     # TODO: create logger in here and put it into debug log
    #     print(f"__repr__ of SoC: {self.name}")
    #     return str(self.__dict__)