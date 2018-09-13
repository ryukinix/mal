#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

# stdlib
import sys
import os
from functools import wraps
from sre_constants import error as BadRegexError
import xml.etree

# 3rd party
from decorating.animation import AnimatedDecorator
from requests.exceptions import ConnectionError

# self-package
from mal import color


def killed():
    """Show a message if user terminated the program."""
    message = ("\n ┑(￣Д ￣)┍ somebody seems killed me..."
               "\nw a s  Y O U ?! ︵ヽ(`Д´)ﾉ︵﻿ ")
    print(color.colorize(message, 'red'), file=sys.stderr)
    os._exit(1)


def print_error(error_name, status, reason, kill=False):
    padding = (len(error_name) + 2) * ' '
    error = color.colorize(error_name, 'red', 'bold')
    status = color.colorize(status, 'cyan')
    print(('{error}: {status}\n'
           '{padding}{reason} ¯\_(ツ)_/¯'.format_map(locals())),
          file=sys.stderr)
    if kill:
        os._exit(1)


# THIS IS A LOL ZONE

#    /\O    |    _O    |      O
#     /\/   |   //|_   |     /_
#    /\     |    |     |     |\
#   /  \    |   /|     |    / |
# LOL  LOL  |   LLOL   |  LOLLOL

# D
#   E
#     C
#       O
#         R
#           A
#             T
#               O
#                 R
#                   S

def checked_regex(func):
    """Wrap the function in a try/except to catch and handle a BadRegexError."""
    @wraps(func)  # keeps the wrapped function's name and docstring intact
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except BadRegexError:
            if AnimatedDecorator.spinner.running:
                AnimatedDecorator.stop()
            print_error('BadRegexError', 'invalid regex', 'reason: you')
            sys.exit(1)

        return result
    return wrapper


def checked_cancer(func):
    """Wrap the function in a try/except to catch and handle a BadRegexError."""
    @wraps(func)  # keeps the wrapped function's name and docstring intact
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except xml.etree.ElementTree.ParseError:
            if AnimatedDecorator.spinner.running:
                AnimatedDecorator.stop()
            print_error('XMLParseError', 'Invalid API Response', 'reason: MAL IS DEAD')
            sys.exit(1)

        return result
    return wrapper




def checked_connection(func):
    """Wrap the function in a try/except to catch and handle a ConnectionError."""
    @wraps(func)  # keeps the wrapped function's name and docstring intact
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except ConnectionError as e:
            if AnimatedDecorator.spinner.running:
                AnimatedDecorator.stop()
            error_name = e.__class__.__name__
            status = e.args[0].__class__.__name__
            reason = e.args[0].reason.__class__.__name__
            print_error(error_name, status, "reason: {}".format(reason))
            sys.exit(1)
        return result

    return wrapper
