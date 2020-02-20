
# Basic object for passing data between threads
import threading


class ThreadCommonObject:
    def __init__(self):

        # Config parameters
        self.config = None

        # Control
        self.shutdown = threading.Event()

        # Data variables

        # Command ready flag event is triggered by the chat_listener. The command_processor waits for it to be set,
        # processes the command, and then clears the flag when ready for another event.
        self.command_ready_flag = threading.Event()
        self.command = ""

        self.command_thread_status = False
        self.chat_listener_thread_stauts = False
