
import logging
import os
import yaml

log = logging.getLogger()

DEFAULT_CONFIG = "config.yaml"
PRIVATE_CONFIG = "private_config.yaml"


class pixel_order:
    def __init__(self, name="RGB", order=(0, 1, 2)):
        self.name = name
        self.order = order
        self.bytes = len(order)


def get_config():
    config = {}
    # Read in configuration values
    # If private config file exists, update / overwrite with those values
    for config_file in [DEFAULT_CONFIG, PRIVATE_CONFIG]:
        if os.path.exists(config_file):
            with open(config_file) as c:
                print("Reading in {} file".format(config_file))
                config.update(yaml.safe_load(c))
        else:
            print("WARNING: Config file \"{}\" does not exist.".format(config_file))
    return config

def load_solid_colors():
    solid_colors = {}
    # read in yaml file  with solid colors
    with open("common/led_colors.yaml") as y:
        solid_colors = yaml.safe_load(y)["solid"]
    # convert lists into tuples (yaml has to store the values as lists, neopixel wants tuples)
    for k, v in solid_colors.items():
        solid_colors[k] = tuple(v)
    return solid_colors

def load_text_responses():
    try:
        with open("common/text_responses.yaml") as t:
            text_responses = yaml.safe_load(t)
    except FileNotFoundError:
        log.error("Text response file not found! Disabling text responses...")
        text_responses = {}
    return text_responses