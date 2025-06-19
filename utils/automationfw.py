import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from drivers.relay_controller import *
from drivers.ssh_controller import *
from drivers.serial_controller import *
from .config_loader import *
from .arg_parser import Args
from .logger import LoggerSetup

class AutoFW:
    def __init__(self):
        self.args = Args.parse_args()
        self.logger = LoggerSetup.get_logger(name=__name__, log_level=self.args.log_level)
        self.logger.debug(self.args)
        self.config = None
        # TODO: update config
        # self.config = ConfigLoader.get_target("")
        # self.ssh_controller = SSHController(self.config["ssh_host"], self.config["ssh_user"], self.config["ssh_pass"])
        self.ssh_controller = SSHController("192.168.36.10", "yzungx", "1")
        self.serial_controller = SerialController("/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0")
        # self.relay_controller = RelayController("need_to_fill_pin_here")
