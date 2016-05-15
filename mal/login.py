#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyleft © Manoel Vilela
#
#

import os
from configparser import ConfigParser
from getpass import getpass

DEFAULT_FILE = '~/.myanimelist.init'
DEFAULT_SECTION = 'mal'
DEFAULT_PATH = os.path.expanduser(DEFAULT_FILE)


def get_credentials():
    config = ConfigParser()
    config.read(DEFAULT_PATH)
    if DEFAULT_SECTION not in config:
        config = create_credentials()

    return config[DEFAULT_SECTION]


def create_credentials():
    print("-- MAL login")
    config = ConfigParser()
    with open(DEFAULT_PATH, 'w') as cfg:
        config.add_section(DEFAULT_SECTION)
        config.set(DEFAULT_SECTION, 'username', input('Username: '))
        config.set(DEFAULT_SECTION, 'password',  getpass())
        config.write(cfg)
        print('-- credentials saved in {}'.format(DEFAULT_PATH))
    return config
