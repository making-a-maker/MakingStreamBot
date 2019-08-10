
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

            with self.tco_lock:
                self.tco.command_ready_flag.clear()

# Proposed commands
# add user
# del user
# colors?
# listen for sub / raid / follow


