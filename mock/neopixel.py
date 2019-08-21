

class NeoPixel:
    def __init__(self, pin, leds, brightness=1.0, auto_write=False):
        self.pin = pin
        self.auto_write = auto_write
        self.leds = leds
        self.brightness = brightness

    def show(self):
        pass

    def fill(self, color):
        pass
