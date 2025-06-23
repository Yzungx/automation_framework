import sys
import os
import pytest
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.automationfw import AutoFW
# TODO: think about move log parser as a util of AutoFW
from utils.log_parser import Log_parser

class TestDay_1():

    def setup_method(self):
        self.autoFw = AutoFW()
        self.pi_3_alias = "raspberry_pi3"
        self.pi_3_dut= self.autoFw.system_testing.dut_objects[self.pi_3_alias]
        self.pi_3_soc_BCM2837 = self.pi_3_dut.soc_objects["BCM2837"]

    def teardown_method(self, method):
        print(f"Tearing down method: {method.__name__}")

    # @pytest.mark.timeout(10)
    def test_ssh(self):
        res = Log_parser.clean_string(self.pi_3_soc_BCM2837.ssh_controller.execCommand('whoami'))
        assert res == self.pi_3_soc_BCM2837.user.account

    def test_scp(self):
        self.pi_3_soc_BCM2837.ssh_controller.scp(
            local_path="/home/yzungx/ws/automation_fw/automation_framework/tests/test_resources/whoami.txt",
            remote_path="/home/yzungx"
            )
        
        res = Log_parser.clean_string(self.pi_3_soc_BCM2837.ssh_controller.execCommand('cat /home/yzungx/whoami.txt'))
        assert res == self.pi_3_soc_BCM2837.user.account

    def test_serial_login(self):
        # TODO: improve reading log
        self.pi_3_soc_BCM2837.serial_controller.open()
        self.pi_3_soc_BCM2837.serial_controller.login(username=self.pi_3_soc_BCM2837.user.account, password=self.pi_3_soc_BCM2837.user.password)

        # res = self.pi_3_soc_BCM2837.serial_controller.send_command_and_get_response("whoami")

        # clean_res = Log_parser.extract_command_output(res, "whoami")

        # assert clean_res == self.pi_3_soc_BCM2837.user.account

        # self.pi_3_soc_BCM2837.serial_controller.safe_exit()

        
        res = self.pi_3_soc_BCM2837.serial_controller.send_command_and_get_response("sudo reboot")
        res = self.pi_3_soc_BCM2837.serial_controller.send_command_and_get_response("1", wait_for="login", timeout=0)

    def test_reboot(self):
        pass




