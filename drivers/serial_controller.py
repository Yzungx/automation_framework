import serial
import time
from typing import final, Optional
from datetime import datetime
import os


@final
class SerialController:
    def __init__(self, port, baudrate=115200, timeout=1, enable_log=True, log_file: Optional[str] = None):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.enable_log = enable_log
        self.log_file = log_file

        if self.enable_log and self.log_file:
            self._init_log_header()

    def _init_log_header(self):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            separator = f"\n{'=' * 60}\n[Session Start: {timestamp}]\n{'=' * 60}\n"
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(separator)
        except Exception as e:
            print(f"[Serial] Log init failed: {e}")
            self.enable_log = False

    def _log(self, message: str):
        now = datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{now}] {message}"
        if self.enable_log:
            print(full_msg)
        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(full_msg + "\n")
            except Exception:
                # Don't raise during cleanup
                pass

    def open(self):
        if self.ser is None or not self.ser.is_open:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            time.sleep(0.1)
            self._log(f"[Serial] Opened port {self.port} at {self.baudrate} baud.")

    def _close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self._log(f"[Serial] Closed port {self.port}.")

    def write_line(self, cmd):
        if self.ser and self.ser.is_open:
            self.ser.write((cmd + '\n').encode())
            self._log(f"[Serial] Sent: {cmd}")

    def read_line(self):
        if self.ser and self.ser.is_open:
            line = self.ser.readline().decode(errors='ignore').strip()
            return line
        return ""

    def read_until(self, pattern, timeout=10):
        start = time.time()
        buffer = ""
        while time.time() - start < timeout:
            line = self.read_line()
            if line:
                self._log(f"[Serial] {line}")
                buffer += line + "\n"
                if pattern in line:
                    return buffer
        raise TimeoutError(f"Pattern '{pattern}' not found")

    # def send_command_and_get_response(self, command, wait_for="$", timeout=3) -> str:
    #     if self.ser is None or not self.ser.is_open:
    #         raise ConnectionError("Serial port not open")

    #     self.ser.write((command + '\n').encode('utf-8'))
    #     time.sleep(0.1)

    #     response = ""
    #     start_time = time.time()
    #     while time.time() - start_time < timeout:
    #         if self.ser.in_waiting:
    #             chunk = self.ser.read(self.ser.in_waiting).decode('utf-8', errors='ignore')
    #             response += chunk
    #             if wait_for in response:
    #                 break
    #         else:
    #             time.sleep(0.1)
    #     self._log(f"[Serial] Response of `{command}`:\n{response.strip()}")
    #     return response.strip()

    def send_command_and_get_response(self, command, wait_for="$", timeout=3) -> str:
        # version 2 with timeout = 0 so wait infinity until meet wait_for
        if self.ser is None or not self.ser.is_open:
            raise ConnectionError("Serial port not open")

        self.ser.write((command + '\n').encode('utf-8'))
        time.sleep(0.1)

        response = ""
        start_time = time.time()

        while True:
            if self.ser.in_waiting:
                chunk = self.ser.read(self.ser.in_waiting).decode('utf-8', errors='ignore')
                response += chunk
                if wait_for in response:
                    break
            else:
                time.sleep(0.1)

            # Check timeout if timeout is greater than 0
            if timeout > 0 and (time.time() - start_time >= timeout):
                self._log(f"[Serial] Timeout waiting for `{wait_for}` in response to `{command}`.")
                break

        self._log(f"[Serial] Response of `{command}`:\n{response.strip()}")
        return response.strip()


    def login(self, username, password):
        self._log("[Serial] Sending user name...")
        self.send_command_and_get_response(username)
        self._log("[Serial] Sending password...")
        self.send_command_and_get_response(password)
        self._log("[Serial] Verifying with 'whoami'...")
        self.send_command_and_get_response("whoami")
        self._log("[Serial] Login successful.")

    def safe_exit(self, timeout: int = 10):
        try:
            if self.ser and self.ser.is_open:
                self._log("[Serial] Sending `exit` to close serial session...")
                res = self.send_command_and_get_response(command="exit", wait_for='', timeout=timeout)
                self._log(f"[Serial] Exit command sent, response:\n{res}")
        except Exception as e:
            self._log(f"[Serial] Safe exit failed: {e}")


    def send_command_and_get_number_of_line(self, command, wait=1, buffer_length: int = 100):
        self.write_line(command)
        time.sleep(wait)
        return "\n".join(self.read_all_lines(max_lines=buffer_length))

    def read_all_lines(self, max_lines=1000):
        lines = []
        for _ in range(max_lines):
            line = self.read_line()
            if line:
                lines.append(line)
                self._log(f"[Serial] {line}")
            else:
                break
        return lines

    def __del__(self):
        try:
            self.safe_exit()
            self._close()
        except Exception:
            pass  # Avoid exceptions during interpreter shutdown
