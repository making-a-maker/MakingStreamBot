
import logging
logger = logging.getLogger()


class NeoPixel:
    def __init__(self, queue, num_leds, brightness=1.0, auto_write=False):
        self.queue = queue
        self.auto_write = auto_write
        self.pixels = [(0, 0, 0)] * num_leds
        self.brightness = brightness
        # ToDo: handle brightness

    def __setitem__(self, key, value: tuple):
        # logger.error("input {}: {}".format(key, value))
        self.pixels[key] = value

    def __getitem__(self, item):
        return self.pixels[item]

    def show(self):
        self.queue.put(self.pixels)

    def fill(self, color):
        for i in range(len(self.pixels)):
            self.pixels[i] = color
        if self.auto_write:
            self.show()


