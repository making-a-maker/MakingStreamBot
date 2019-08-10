#! /usr/bin/python3


import argparse
import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
import os
import signal
import sys
import threading
import time
import traceback
import yaml

import chat_listener.listener as listener
import command_processor.commander as commander
from streammonitor.ThreadCommonObject import ThreadCommonObject
from utils.log_format import ColorFormatter

VERSION = "0.0.1"

program_name = "streammonitor"

DEFAULT_CONFIG = "config.yaml"
PRIVATE_CONFIG = "private_config.yaml"


##############################
# Command Line Arguments
# and Config File Handling
##############################
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Supply the path to an alternate config file\n "
                                           "This config parameter will override defaults if keys match")
args = parser.parse_args()

if args.config:
    config_file = args.config
else:
    config_file = PRIVATE_CONFIG

config = {}
# Read in configuration values
if os.path.exists(DEFAULT_CONFIG):
    with open("config.yaml") as pc:
        print("Reading in config.yaml file")
        config.update(yaml.unsafe_load(pc.read()))
# If private config file exists, update with those values (private overrides public)
if os.path.exists(config_file):
    with open(config_file) as pc:
        print("Reading in {} file".format(config_file))
        config.update(yaml.unsafe_load(pc.read()))
else:
    print("WARNING: Config file \"{}\" does not exist.".format(config_file))

#########################
# Logging
#########################

log_default_level = "INFO"
if "log_default_level" in config.keys():
    log_default_level = getattr(logging, config["log_default_level"].upper(), None)

# Custom ANSI colors for log level names in logs
formatter = ColorFormatter("{asctime} {threadName} {levelname} {message}", style="{")

# Get logging level from config file, if it exists
try:
    log_file_enabled = config["log_file_enabled"]
    log_file = config["log_file_directory"] + program_name + ".log"
    log_file_level = getattr(logging, config["log_file_level"].upper(), None)

    log_console_enabled = config["log_console_enabled"]
    log_console_level = getattr(logging, config["log_console_level"].upper(), None)

    print("Logging set by config file")

except KeyError as e:
    print("Log setup from config has failed!!\n", type(e).__name__, e.args, traceback.format_exc())
    log_file = "/tmp/" + program_name + ".log"
    log_level = "INFO"
    log_file_enabled = False
    log_console_enabled = True
    print("Logging using default values:\nLog File: {}  Log Level: {}\nFile Logging: {}  Console Logging: {}\n".format(
        log_file, log_level, log_file_enabled, log_console_enabled))


# The main logger instance
logger = logging.getLogger()
logger.setLevel(log_default_level)

# Set up handlers if they are enabled
# File handler
if log_file_enabled:
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_file, when="D", interval=7, backupCount=10)
    file_handler.setLevel(getattr(logging, config["log_file_level"].upper(), None))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

if log_console_enabled:
    console_handler = StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, config["log_console_level"].upper(), None))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Let's kick off the logging right...
logger.critical("This is the beginning of the log...")


# set up command line interrupt signal handler (if desired)

# set up thread common object for data relay
#    commands detected info
#    logging object
#    config details

tco = ThreadCommonObject()
tco_lock = threading.Lock()
with tco_lock:
    tco.logger = logger
    tco.config = config


def signal_handler(signum, frame):
    """
    """
    global tco
    logger.debug("SIGNAL: {}\nFRAME: {}".format(signum, frame))
    logger.critical("USER COMMANDED SHUT DOWN")
    with tco.lock:
        tco.shutdown = True


signal.signal(signal.SIGINT, signal_handler)


# set up threads
#   chat listener (connect to channel, listen to chat, if keyword is found, store in TCO, and set event)
#   command processor (wait for event from chat_listener thread, or shutdown event from main, and execute commands)
#   command line interface? Do I need this? might be nice to trigger events from CL, without having to involve
#     twitch chat)
#
ready = threading.Barrier(3, timeout=10)
# ready = ""
chat_thread = listener.ChatListener(tco, tco_lock, ready)
command_thread = commander.CommandProcessor(tco, tco_lock, ready)
logger.info("Thread are initialized... Starting threads")

# start threads
chat_thread.start()
command_thread.start()
ready.wait()
logger.info("Thread Report Ready")

# wait for threads to join
chat_thread.join()
command_thread.join()

