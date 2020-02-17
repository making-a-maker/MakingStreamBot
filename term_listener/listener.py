

#
from datetime import datetime
import logging
import serial
import socket
import traceback
import threading

from utils.log_colors import colors as c

logger = logging.getLogger()

command_characters = ("!", "#")

TIMER_DELAY = 31.0

num_hais = 0


class SerialListener(threading.Thread):

    def __init__(self, tco, tco_lock, ready):

        logger.info("Initializing Serial Listener")

        super().__init__()
        self.name = "Serial Listener"

        self.tco = tco
        self.tco_lock = tco_lock

        with self.tco_lock:
            self.config = tco.config
            self.shutdown = tco.shutdown

        self.socket = None

        self.ready = ready

    def run(self):
        logger.info("Term Listener started running")

        # Barrier event to trigger when threads are ready to go
        logger.warning("**** TERM LISTENER thread waiting on ready")
        self.ready.wait()

        with self.tco_lock:
            self.tco.term_listener_thread_status = True

        # timer_chat_stop = threading.Event()
        # self.timer_chat(timer_chat_stop)

        response = ""

        while not self.shutdown.is_set():
            try:

                msg = input(response).strip()

                if msg == "exit":
                    break

                if msg.message.startswith(("!", )):
                    logger.debug("HEARD A COMMAND - User: {}  Command: {}".format("TERM", msg.message))
                    with self.tco_lock:
                        self.tco.command = "TERM", msg.message
                        self.tco.command_ready_flag.set()

            except Exception as e:
                logger.error(type(e).__name__, e.args, traceback.format_exc())
        return 0

    def chat(self, message):
        logger.debug("Term Listener >: {}".format(message))

    def timer_chat(self, stop):

        global num_hais

        # print("{} - Sending Hai - {}".format(datetime.now(), num_hais))
        self.chat("Hai Hai - {}".format(num_hais))
        num_hais += 1

        if not stop.is_set():
            threading.Timer(TIMER_DELAY, self.timer_chat, [stop]).start()


