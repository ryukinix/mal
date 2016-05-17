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
from mal.api import MyAnimeList
from mal import color

DEFAULT_FILE = '~/.myanimelist.init'
DEFAULT_SECTION = 'mal'
DEFAULT_PATH = os.path.expanduser(DEFAULT_FILE)

LOGIN_HEADER = color.colorize("-- MAL login", 'cyan')
SUCCESSFUL = color.colorize(':: valid credentials!', 'green')
INVALID = color.colorize(':: invalid credentials! try again', 'red')


def get_credentials():
    config = ConfigParser()
    config.read(DEFAULT_PATH)
    if DEFAULT_SECTION not in config:
        config = create_credentials()

    return config[DEFAULT_SECTION]


def create_credentials():
    print(LOGIN_HEADER)
    config = ConfigParser()
    config.add_section(DEFAULT_SECTION)
    config.set(DEFAULT_SECTION, 'username', input('Username: '))
    config.set(DEFAULT_SECTION, 'password',  getpass())
    if MyAnimeList.login(config['mal']):
        with open(DEFAULT_PATH, 'w') as cfg:
            config.write(cfg)
            print(SUCCESSFUL, 'saved in {}'.format(DEFAULT_PATH))
    else:
        print(INVALID)
        config = create_credentials()
    return config
