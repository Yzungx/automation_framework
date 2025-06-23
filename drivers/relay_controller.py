import subprocess
from typing import Optional, Dict

class USBRelayController:
    def __init__(self, relay_name: Optional[str] = None, timeout: int = 5):
        """
        Initializes the USB relay controller.

        Args:
            relay_name (str): The specific relay name (e.g., 'ID01_1').
                              If not provided, the first available relay will be used.
            timeout (int): Timeout for subprocess execution in seconds.
        """
        self.relay_name = relay_name
        self.timeout = timeout

    def _run_command(self, args: str) -> subprocess.CompletedProcess:
        """
        Executes a usbrelay command via subprocess.

        Args:
            args (str): Command-line arguments to pass to usbrelay.

        Returns:
            CompletedProcess: Result of the subprocess execution.
        """
        try:
            return subprocess.run(
                f"usbrelay {args}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout,
                text=True
            )
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"[USB Relay] Command timeout: usbrelay {args}")
        except Exception as e:
            raise RuntimeError(f"[USB Relay] Command error: {e}")

    def list_relays(self) -> Dict[str, str]:
        """
        Lists all connected USB relay devices and their statuses.

        Returns:
            Dict[str, str]: Dictionary mapping relay IDs to their current states ('0' or '1').
        """
        result = self._run_command("")
        lines = result.stdout.strip().splitlines()
        relays = {}
        for line in lines:
            if "=" in line:
                relay_id, status = line.split("=")
                relays[relay_id.strip()] = status.strip()
        return relays

    def _ensure_relay_name(self):
        """
        Ensures that a relay name is available.
        If not set, selects the first available one from list_relays().
        """
        if not self.relay_name:
            relays = self.list_relays()
            if not relays:
                raise ValueError("No USB relay devices found.")
            self.relay_name = next(iter(relays))

    def turn_on(self) -> bool:
        """
        Turns the relay ON.

        Returns:
            bool: True if successful, False otherwise.
        """
        self._ensure_relay_name()
        result = self._run_command(f"{self.relay_name}=1")
        return result.returncode == 0

    def turn_off(self) -> bool:
        """
        Turns the relay OFF.

        Returns:
            bool: True if successful, False otherwise.
        """
        self._ensure_relay_name()
        result = self._run_command(f"{self.relay_name}=0")
        return result.returncode == 0
