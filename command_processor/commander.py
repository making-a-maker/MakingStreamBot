
import logging
import threading
# import traceback

import board
import neopixel

from utils.led_colors import solid

logger = logging.getLogger()



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
        self.cmd = ""
        self.ready = ready

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

            self.cmd = self.command[1].strip("!")
            if self.cmd in solid.keys():
                self.solid_color(solid[self.cmd])

            with self.tco_lock:
                self.tco.command_ready_flag.clear()

# Proposed commands
# add user
# del user
# colors?
# listen for sub / raid / follow
    def display(self, pattern):
        pass

    def solid_color(self, color: tuple):
        self.pixels.fill(color)
        self.pixels.show()

