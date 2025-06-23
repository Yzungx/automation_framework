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
class Log_parser:

    @staticmethod
    def clean_string(str: str):
        """
            clean \n, \r\n and blank space in head and tail of string 
        """
        return str.strip()
    
    @staticmethod
    def extract_command_output(raw: str, command: str, prompt_pattern: str = r'\w+@[\w\-]+:.*\$') -> str:

        ANSI_ESCAPE_PATTERN = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        raw = ANSI_ESCAPE_PATTERN.sub('', raw)  # Clean escape characters

        lines = [line.strip() for line in raw.strip().splitlines() if line.strip()]
        output_lines = []
        found_cmd = False

        for line in lines:
            if not found_cmd:
                if line == command:
                    found_cmd = True
            else:
                if re.match(prompt_pattern, line):
                    break
                output_lines.append(line)

        return " ".join(output_lines).strip()

