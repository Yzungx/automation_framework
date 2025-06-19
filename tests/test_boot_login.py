import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.automationfw import AutoFW

class TestDay_1():

    def setup_method(self):
        self.autoFw = AutoFW()
        # self.fw.setup_firmware()

    def teardown_method(self, method):
        print(f"Tearing down method: {method.__name__}")

    # @pytest.mark.timeout(10)
    def test_board_ssh_and_login(self):
        self.autoFw.logger.debug("test logger debug")
        res = self.autoFw.ssh_controller.execCommand('ls')
        self.autoFw.logger.info(f"res:  {res}")
        # print(f"res:  {res}")
        assert 2 + 2 == 4
