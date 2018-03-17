#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

# stdlib
import os
from os import path
from configparser import RawConfigParser

# 3rd party
from appdirs import user_config_dir
import decorating

# self-package
from mal import __name__ as APP_NAME

# variables for proper saving
APP_FILE = 'myanimelist.ini'
APP_DIR = user_config_dir(APP_NAME)
CONFIG_PATH = path.join(APP_DIR, APP_FILE)
LOGIN_SECTION = 'login'
CONFIG_SECTION = 'config'
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_CONFIG = {
    CONFIG_SECTION: {
        'date_format': DEFAULT_DATE_FORMAT,
        'animation': True,
    },
}


def config():
    """Create a RawConfigParser and if exists read it before return

    :returns: the current config or a new one
    :rtype: configparser.RawConfigParser
    """
    parser = RawConfigParser()
    if path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            parser.read_file(f)

    if CONFIG_SECTION not in parser:
        parser.read_dict(DEFAULT_CONFIG)
        # ensure that directory app_dir exists or creates otherwise
        os.makedirs(APP_DIR, exist_ok=True)
        with open(CONFIG_PATH, 'w') as f:
            parser.write(f)
    elif 'animation' not in parser[CONFIG_SECTION]:
        parser.set(CONFIG_SECTION, 'animation', True)
        with open(CONFIG_PATH, 'w') as f:
            parser.write(f)

    return parser


@decorating.cache
def date_format():
    """Get current date format from config file"""
    return config()['date_format']


def print_config():
    """Print current config and its PATH"""
    print("File on: {}".format(CONFIG_PATH))
    with open(CONFIG_PATH, 'r') as f:
        print(f.read())
