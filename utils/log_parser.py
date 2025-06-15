import re
import time

def wait_for_log_pattern(serial_controller, pattern, timeout=30):
    regex = re.compile(pattern)
    start = time.time()
    while time.time() - start < timeout:
        line = serial_controller.read_line()
        if line:
            print(f"[Serial] {line}")
            if regex.search(line):
                return True
    return False
