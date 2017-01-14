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
from os import makedirs
from configparser import ConfigParser
from getpass import getpass

# 3rd party
from appdirs import user_config_dir

# self-package
from mal.api import MyAnimeList
from mal import color
from mal import __name__ as APP_NAME

# variables for proper saving
APP_FILE = 'myanimelist.ini'
APP_DIR = user_config_dir(APP_NAME)
APP_PATH = path.join(APP_DIR, APP_FILE)
LOGIN_SECTION = 'login'

# logging messages
LOGIN_HEADER = color.colorize("-- MAL login", 'cyan')
SUCCESSFUL = color.colorize(':: valid credentials!', 'green')
INVALID = color.colorize(':: invalid credentials! try again', 'red')


def get_credentials():
    """Fetch the username and password from the right file."""
    config = ConfigParser()
    config.read(APP_PATH)
    if LOGIN_SECTION not in config:
        config = create_credentials()

    return config[LOGIN_SECTION]


def create_credentials():
    print(LOGIN_HEADER)
    config = ConfigParser()
    config.add_section(LOGIN_SECTION)
    config.set(LOGIN_SECTION, 'username', input('Username: '))
    config.set(LOGIN_SECTION, 'password',  getpass())
    if MyAnimeList.login(config[LOGIN_SECTION]):
        makedirs(APP_DIR, exist_ok=True)
        with open(APP_PATH, 'w') as cfg:
            config.write(cfg)
            print(SUCCESSFUL, 'saved in {}'.format(APP_PATH))
    else:
        print(INVALID)
        config = create_credentials()
    return config
