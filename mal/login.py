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
from mal import color
from mal import setup
from mal import auth


def get_credentials():
    """Fetch the username and password from the right file."""
    config = setup.config()
    if setup.LOGIN_SECTION not in config:
        config = create_credentials()

    return config


def create_credentials():
    # logging messages
    login_header = color.colorize("-- MAL login", 'cyan')
    print(login_header)

    config = setup.config()
    if setup.LOGIN_SECTION not in config:
        config.add_section(setup.LOGIN_SECTION)
    token = auth.login()
    config.set(setup.LOGIN_SECTION, 'token', token)
    with open(setup.CONFIG_PATH, 'w') as cfg:
        config.write(cfg)
        print(color.colorize("-- OAuth2 token saved!", 'cyan'))

    return config
