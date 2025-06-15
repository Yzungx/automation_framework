import sys
import os
import pytest

from drivers.relay_controller import RelayController
from drivers.serial_controller import SerialController
from drivers.ssh_controller import SSHController
from utils.config_loader import load_config
from utils.log_parser import wait_for_log_pattern
from utils.logger import *

if __name__ == "__main__":

    try:
        # Create an instance of LoggerSetup
        logger_setup = LoggerSetup()
    
        # Configure logging
        logger_setup.configure_logging()
    
        # Log example messages
        logger_setup.log_example_messages()
        config = load_config("/home/yzungx/ws/automation_fw/automation_framework/config/device_config.yaml")
        print(config)
    #     ssh = SSHController(config["ssh_host"], config["ssh_user"], config["ssh_pass"])

    #     print(ssh.execCommand("ls"))

    #     print(ssh.scp(local_path="/home/yzungx/ws/automation_fw/automation_framework/config/device_config.yaml",
    #                  remote_path="/home/yzungx"))
        serial = SerialController("/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0")
        serial.open()

        # Auto login
        serial.login(username="yzungx", password="1")
        print(serial.send_command_and_get_number_of_line("/home/yzungx/print", wait=1, buffer_length=200))

        # serial.close()
    except Exception as e:
        print(f"An error occurred: {e}")


