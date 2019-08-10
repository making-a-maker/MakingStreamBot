

#
from datetime import datetime
import logging
import signal
import socket
import sys
import traceback
import threading

from utils.common import read_message
from utils.log_colors import colors as c

logger = logging.getLogger()

command_characters = ("!", "#")

TIMER_DELAY = 31.0

num_hais = 0


class ChatListener(threading.Thread):

    def __init__(self, tco, tco_lock, ready):

        logger.info("Initializing Chat Listener")

        super().__init__()
        self.name = "Listener"

        self.tco = tco
        self.tco_lock = tco_lock

        with self.tco_lock:
            self.config = tco.config
            self.shutdown = tco.shutdown

        self.socket = None

        self.ready = ready

    def run(self):
        logger.info("Chat Listener started running")
        # signal.signal(signal.SIGINT, signal_handler)

        logger.info("Listener is opening socket and joining room...")
        self.socket = self.open_socket()
        self.join_room(self.socket)

        # Barrier event to trigger when threads are ready to go
        logger.warning("**** LISTENER thread waiting on ready")
        self.ready.wait()

        with self.tco_lock:
            self.tco.chat_listener_thread_status = True

        timer_chat_stop = threading.Event()
        self.timer_chat(timer_chat_stop)

        try:
            while not self.shutdown.is_set():
                response = self.socket.recv(1024).decode()

                if response == "PING :tmi.twitch.tv\r\n":
                    self.socket.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
                    logger.info("{}Pinged by twitch, ponging.. {}".format(c['c'], c['x']))

                else:
                    msg = read_message(response)

                    # ToDo: Need to account for a RECONNECT command from IRC - needs to close and reconnect the socket.

                    if msg.message.startswith(tuple(self.config["command_characters"])):
                        logger.info("HEARD A COMMAND - User: {}  Command: {}".format(msg.user, msg.message))
                        with self.tco_lock:
                            self.tco.command = msg.user, msg.message
                            self.tco.command_ready_flag.set()

        except Exception as e:
            self.socket.close()
            logger.critical("{} Lost connection to Twitch IRC {}".format(c['r'], c['x']))
            logger.error(type(e).__name__, e.args, traceback.format_exc())

            exit(1)

        return 0

    def chat(self, message):
        message_temp = "PRIVMSG #{} :{}".format(self.config["channel"], message)
        logger.info("< {}".format(message_temp))
        self.socket.send((message_temp + "\r\n").encode())

    def timer_chat(self, stop):

        global num_hais

        # print("{} - Sending Hai - {}".format(datetime.now(), num_hais))
        self.chat("Hai Hai - {}".format(num_hais))
        num_hais += 1

        if not stop.is_set():
            threading.Timer(TIMER_DELAY, self.timer_chat, [stop]).start()

    def open_socket(self):
        s = socket.socket()
        s.connect((self.config["host"], self.config["port"]))
        s.send("CAP REQ :twitch.tv/commands\r\n".encode())
        s.send(("PASS {}\r\n".format(self.config["pass"])).encode())
        s.send(("NICK {}\r\n".format(self.config["nick"])).encode())
        s.send(("JOIN #{}\r\n".format(self.config["channel"])).encode())
        s.send("CAP REQ :twitch.tv/commands twitch.tv/tags\r\n".encode())
        return s

    def join_room(self, s):
        readbuffer = ""
        loading = True
        while loading:
            readbuffer = readbuffer + s.recv(1024).decode()
            temp = (readbuffer.split("\r\n"))
            readbuffer = temp.pop()

            for line in temp:
                logger.debug("+ {}".format(line))
                if "End of /NAMES list" in line:
                    loading = False
        self.chat(str(datetime.utcnow()) + " - Successfully joined chat")


'''
def signal_handler(signum, frame):
    """
    Displays a menu when the user inputs ctrl+c
    """
    print("Flagged: {}\nFrame: {}".format(signum, frame))
    print("\nPaused:\n\t1 = Message\n\t2 = Timeout User\n\tq = Quit")
    cmd = input("\nCommand: ")
    if cmd == 'q':
        chat(s, "Disconnected")
        # ToDo: fix reference to channel
        s.send("PART {}\r\n".format("#making_a_maker").encode("utf-8"))
        print("Exitting MrLoLBot..")
        sys.exit(0)
    elif cmd == '1':
        message = input("Message to send: ")
        chat(s, message)
        print("Message Sent")
    elif cmd == '2':
        username = input("User to timeout: ")
        timeout(s, username)
        print("Timing out: {}".format(username))
    print("\nResuming..\n")
'''
