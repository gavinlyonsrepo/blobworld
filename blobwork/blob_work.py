""" module imported into blobworld containing functions for various utilises"""

# === IMPORTS ===

import configparser
import sys
import os
import logging
import datetime
from pathlib import Path

# === CLASSES ===


class BlobWorldConfigFile:
    """Class to handle config file reading
    and creation, called before logging"""
    def __init__(self, name):
        self.name = name
        if sys.platform == 'win32':
            home_path = os.environ['HOMEPATH']
        else:
            home_path = os.environ['HOME']
        self.config_file_path = Path(home_path + "/.config/blobworld")
        # blobs
        self.starting_red_blobs = 10
        self.starting_green_blobs = 10
        self.starting_blue_blobs = 10
        self.max_size_blob = 20
        # screen
        self.screen_width = 800
        self.screen_height = 600
        self.clock_tick = 60  # frames per second max
        self.back_ground_color = 'BEIGE'
        # log
        self.logging_on_off = "off"
        self.log_file_path = Path('/tmp/')

    def create_configfile_func(self):
        """ creates a config file with default values if missing"""
        # Check config path is there
        if not os.path.exists(self.config_file_path):
            os.makedirs(self.config_file_path)
        config_file_path = self.config_file_path / "blobworld.cfg"
        if os.path.isfile(config_file_path):  # Check config file is there
            pass  # Configfile is there
        else:
            try:  # Create the missing configfile with some defaults
                config = configparser.ConfigParser()
                config['BLOBS'] = {'starting_red_blobs': 10,
                                   'starting_green_blobs': 10,
                                   'starting_blue_blobs': 10,
                                   'max_size_blob': 20}
                config['SCREEN'] = {'screen_width': 800,
                                    'screen_height': 600,
                                    'clock_tick': 60,
                                    'back_ground_color': 'BEIGE'}
                config['LOG'] = {'logging_on_off': 'off',
                                 'log_file_path': self.log_file_path}
                with open(config_file_path, 'w', encoding="utf-8") as configfile:
                    config.write(configfile)
            except Exception as error:
                print("Config file is missing at " + str(config_file_path))
                print("Problem trying to create config file: " + str(error))
            else:
                print("Config file was missing at " + str(config_file_path))
                print("Config file created with default values.")

    def read_configfile_func(self):
        """Read in configfile"""
        try:
            my_config_file = configparser.ConfigParser()
            config_file_path = self.config_file_path / "blobworld.cfg"
            my_config_file.read(config_file_path)
            self.starting_red_blobs = my_config_file.getint(
                "BLOBS", "starting_red_blobs")
            self.starting_green_blobs = my_config_file.getint(
                "BLOBS", "starting_green_blobs")
            self.starting_blue_blobs = my_config_file.getint(
                "BLOBS", "starting_blue_blobs")
            self.max_size_blob = my_config_file.getint("BLOBS", "max_size_blob")
            self.screen_width = my_config_file.getint("SCREEN", "screen_width")
            self.screen_height = my_config_file.getint("SCREEN", "screen_height")
            self.clock_tick = my_config_file.getint("SCREEN", "clock_tick")
            self.back_ground_color = my_config_file.get("SCREEN", "back_ground_color")
            self.logging_on_off = my_config_file.get("LOG", "logging_on_off")
            self.log_file_path = Path(my_config_file.get("LOG", "log_file_path"))
            sum_blobs = self.starting_red_blobs + \
                        self.starting_green_blobs + self.starting_blue_blobs
            if sum_blobs <= 1 or sum_blobs >= 150:
                print("config file sum " + sum_blobs)
                print("Cfg file: sum values blobs must between 1 & 150")
                sys.exit()
        except Exception as error:
            print(" Problem reading in config file: " + str(error))

# === FUNCTIONS ===


def my_logging(module_name):
    """Function to carry out logging"""
    if not os.path.exists(my_cfg_file.log_file_path):
        os.makedirs(my_cfg_file.log_file_path)
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    if my_cfg_file.logging_on_off == "on":
        basename = "BlobWorld"
        suffix = datetime.datetime.now().strftime("%d%m%y_%H%M%S" + ".log")
        # e.g. filename = 'BlobWorld_120508_171442.log'
        filename = "_".join([basename, suffix])
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
        file_handler = logging.FileHandler(my_cfg_file.log_file_path / filename)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    elif my_cfg_file.logging_on_off == "off":
        logger.disabled = True

    return logger


def start(text):
    """import code"""
    my_cfg_file.create_configfile_func()
    my_cfg_file.read_configfile_func()
    logger = my_logging(__name__)
    logger.info(text)


# === MAIN ===
my_cfg_file = BlobWorldConfigFile("config_file")

if __name__ == '__main__':
    start("Main")
else:
    start(" Imported " + __name__)

# === END ===
