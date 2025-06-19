import sys
import os
from typing import final

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from 

@final
class RelayController:
    def __init__(self, pin: any, args: any = None):
        self.pin = pin
        self.args = args
        

    def power_on(self):
        print(f"[Relay] Power ON at pin {self.pin}")

    def power_off(self):
        print(f"[Relay] Power OFF at pin {self.pin}")
