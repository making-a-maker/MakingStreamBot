

import os
import yaml


DEFAULT_CONFIG = "config.yaml"
PRIVATE_CONFIG = "private_config.yaml"

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




