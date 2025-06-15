class RelayController:
    def __init__(self, gpio_pin):
        self.pin = gpio_pin

    def power_on(self):
        print(f"[Relay] Power ON at pin {self.pin}")

    def power_off(self):
        print(f"[Relay] Power OFF at pin {self.pin}")
