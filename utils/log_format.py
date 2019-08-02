
"""
Custom log colors - will colorize log level of messages
Uses ANSI colors
"""

import logging

from utils.colors import *

# Custom ANSI colors for logs
logging_levels = {"DEBUG": CYAN + "DEBUG" + CLEAR,
                  "INFO": LIGHT_GREY + "INFO" + CLEAR,
                  "WARNING": YELLOW + "WARNING" + CLEAR,
                  "ERROR": RED + "ERROR" + CLEAR,
                  "CRITICAL": BOLD_ON + INV_ON + RED + "CRITICAL" + CLEAR}


class ColorFormatter(logging.Formatter):
    def format(self, record):
        # Convert the record object to a string
        r = super().format(record=record)

        # Replace the Logging Level with the colorized version
        if record.levelname in logging_levels.keys():
            r = r.replace(record.levelname, logging_levels[record.levelname])
        return r

