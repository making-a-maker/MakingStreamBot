
import logging
import threading
# import traceback
from utils.led_colors import solid
from command_processor import command_processor as cp

logger = logging.getLogger()
leds_enabled = True

try:
    import board
    import neopixel
except ImportError as e:
    logger.critical("board or neopixel modules not installed - disabling LED string")
    leds_enabled = False


class CommandProcessor(threading.Thread):

    def __init__(self, tco, tco_lock, ready):

        super().__init__()
        self.name = "Commander"

        self.tco = tco
        self.tco_lock = tco_lock

        with self.tco_lock:
            self.config = self.tco.config
            self.shutdown = self.tco.shutdown
            self.command_ready_flag = self.tco.command_ready_flag

        self.command = ()
        self.ready = ready

        if leds_enabled:
            self.pixels = neopixel.NeoPixel(board.D18, self.config["num_leds"],
                                            brightness=self.config["led_brightness"], auto_write=False)

    def run(self):

        # Barrier event to trigger when threads are ready to go
        logger.warning("**** COMMAND thread waiting on ready")
        self.ready.wait()

        with self.tco_lock:
            self.tco.command_thread_status = True

        while not self.shutdown.is_set():
            self.command_ready_flag.wait()
            logger.warning("COMMAND EVENT RECEIVED - Processing...")
            with self.tco_lock:
                self.command = self.tco.command

            logger.info("COMMAND = {}".format(self.command))

            logger.info("Processing command...")

            # Strip off first character of command
            cmd = self.command[1][1:]

            if leds_enabled:
                if cmd in solid.keys():
                    cp.led_process(self.pixels, cmd)
                if cmd in ["pride", "rainbow"]:
                    for i in range(len(self.config["num_leds"])):
                        self.pixels[i] = wheel(i)
                        self.pixels.show()

            with self.tco_lock:
                self.tco.command_ready_flag.clear()

# Proposed commands
# add user
# del user
# colors?
# listen for sub / raid / follow
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

