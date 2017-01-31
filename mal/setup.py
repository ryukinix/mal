#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

# stdlib
from os import path
from configparser import ConfigParser
from datetime import datetime

# 3rd party
from appdirs import user_config_dir

# self-package
from mal import __name__ as APP_NAME

# variables for proper saving
APP_FILE = 'myanimelist.ini'
APP_DIR = user_config_dir(APP_NAME)
CONFIG_PATH = path.join(APP_DIR, APP_FILE)
LOGIN_SECTION = 'login'
CONFIG_SECTION = 'config'
DEFAULT_CONFIG = {
    CONFIG_SECTION: {
        # needs double % because ConfigParser interpolation
        # just one throw an exception
        'date_format': '%%Y-%%m-%%d',
    },
}


def config():
    """Create a ConfigParser and if exists read it before return

    :returns: the current config or a new one
    :rtype: configparser.ConfigParser
    """
    parser = ConfigParser()
    if path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            parser.read_file(f)

    if CONFIG_SECTION not in parser:
        parser.read_dict(DEFAULT_CONFIG)
        with open(CONFIG_PATH, 'w') as f:
            parser.write(f)

    return parser


def date_format():
    """Get current date format from config file"""
    return config()['date_format']


def print_config():
    """Print current config and its PATH"""
    print("File on: {}".format(CONFIG_PATH))
    with open(CONFIG_PATH, 'r') as f:
        print(f.read())
