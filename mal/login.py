#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

# stdlib
from os import makedirs
from getpass import getpass

# self-package
from mal.api import MyAnimeList
from mal import color
from mal import setup


def get_credentials():
    """Fetch the username and password from the right file."""
    config = setup.config()
    if setup.LOGIN_SECTION not in config:
        config = create_credentials()

    return config


def create_credentials():
    # logging messages
    login_header = color.colorize("-- MAL login", 'cyan')
    successful = color.colorize(':: valid credentials!', 'green')
    invalid = color.colorize(':: invalid credentials! try again', 'red')
    print(login_header)

    config = setup.config()
    if setup.LOGIN_SECTION not in config:
        config.add_section(setup.LOGIN_SECTION)
    config.set(setup.LOGIN_SECTION, 'username', input('Username: '))
    config.set(setup.LOGIN_SECTION, 'password',  getpass())

    # confirm that account credentials are correct by trying to log in
    if MyAnimeList.login(config):
        # account is ok, create a config file
        with open(setup.CONFIG_PATH, 'w') as cfg:
            config.write(cfg)
            print(successful, 'saved in {}'.format(setup.CONFIG_PATH))
    else:
        print(invalid)
        config = create_credentials()
    return config
