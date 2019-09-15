
import logging
import queue
from tkinter import *

logger = logging.getLogger()


class GUIHandler:
    def __init__(self, tco, tco_lock):
        self.master = Tk()
        self.master.title("Making A Maker - LED Simulator")

        with tco_lock:
            self.config = tco.config
            self.queue = tco.gui_queue

        self.leds = {
            "num": self.config["num_leds"],
            "string_width": self.config["num_leds"] * self.config["led_sim"]["width"],
            "width": self.config["led_sim"]["width"],
            "height": self.config["led_sim"]["height"],
            "refresh": self.config["led_sim"]["gui_update"]
        }

        logger.debug("Creating canvas")
        self.canvas = Canvas(self.master, width=self.leds["string_width"],
                             height=self.leds["height"], bg="black")
        self.canvas.pack()

        self.pixels = []
        for i in range(self.leds["num"]):
            self.pixels.append(
                self.canvas.create_rectangle(self.leds["width"] * i, 0,
                                             self.leds["width"] * i + self.leds["width"], self.leds["height"],
                                             fill="black")
            )

        self.canvas.update_idletasks()

        self.update_gui()

    def update_gui(self):
        try:
            leds = self.queue.get(block=False)
            for i in range(len(leds)):
                self.canvas.itemconfig(self.pixels[i], fill=self.tk_rgb(leds[i]))

        except queue.Empty:
            pass

        finally:
            self.canvas.after(self.leds["refresh"], self.update_gui)

    @staticmethod
    def tk_rgb(color: tuple):
        return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
