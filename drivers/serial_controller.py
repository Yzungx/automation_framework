import serial
import time
from typing import final

@final
class SerialController:
    def __init__(self, port, baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def open(self):
        if self.ser is None or not self.ser.is_open:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            time.sleep(0.1)
            print(f"[Serial] Opened port {self.port} at {self.baudrate} baud.")

    def _close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"[Serial] Closed port {self.port}.")

    def write_line(self, cmd):
        if self.ser and self.ser.is_open:
            self.ser.write((cmd + '\n').encode())
            print(f"[Serial] Sent: {cmd}")

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
                print(f"[Serial] {line}")
                buffer += line + "\n"
                if pattern in line:
                    return buffer
        raise TimeoutError(f"Pattern '{pattern}' not found")
    
    def send_command_and_get_response(self, command, wait_for="$", timeout=3) -> str:
        self.ser.write((command + '\n').encode('utf-8'))
        time.sleep(0.1)

        response = ""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.ser.in_waiting:
                chunk = self.ser.read(self.ser.in_waiting).decode('utf-8', errors='ignore')
                response += chunk
                if wait_for in response:
                    break
            else:
                time.sleep(0.1)
        print(f"[Serial] Response of `{command}`:\n{response.strip()}")
        return response.strip()


    def login(self, username, password):
        """Login UART terminal"""
        print("[Serial] Sending user name...")
        self.send_command_and_get_response(username)
        print("[Serial] Sending password...")
        self.send_command_and_get_response(password)

        print("[Serial] Test serial is ready to use...")
        self.send_command_and_get_response("whoami")

        print("[Serial] Login successful.")

    def safe_exit(self, timeout: int = 10):
        if self.ser and self.ser.is_open:
            print("[Serial] Exit serial promt...")
            self.send_command_and_get_response(command="exit", wait_for='exit', timeout=timeout)

    def send_command_and_get_number_of_line(self, command, wait=1, buffer_length: int = 100):
        """Send command and get response"""
        self.write_line(command)
        time.sleep(wait)
        return "\n".join(self.read_all_lines(max_lines=buffer_length))

    def read_all_lines(self, max_lines=1000):
        lines = []
        for _ in range(max_lines):
            line = self.read_line()
            if line:
                lines.append(line)
            else:
                break
        return lines
    
    def __del__(self):
        """
            Destructor to ensure the Serial connection is closed when the object is destroyed.
        """
        self.safe_exit()
        self._close()
