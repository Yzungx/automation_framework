from typing import Dict, List
from drivers.ssh_controller import *
from drivers.serial_controller import *

class SOC:
    def __init__(self, name: str, data: Dict):
        self.name = name
        self.ssh_controller = None
        self.serial_controller = None

    def init_resources(self):
        
        # TODO: create pool of ssh tunnel
        self.ssh_controller = SSHController(self.network.ip, self.user.account, self.user.password)
        self.serial_controller = SerialController(
            self.serial.device_file,
            baudrate=self.serial.baudrate,
            enable_log=True, log_file=self.log_path
            )
        
        # Test in local file

        # print(self.ssh_controller.execCommand('ls'))
        # self.serial_controller.open()
        # self.serial_controller.login(username=self.user.account, password=self.user.password)
        # print(self.serial_controller.send_command_and_get_number_of_line("/home/yzungx/print", wait=1, buffer_length=200))

    # def __repr__(self):
    #     # TODO: create logger in here and put it into debug log
    #     print(f"__repr__ of SoC: {self.name}")
    #     return str(self.__dict__)