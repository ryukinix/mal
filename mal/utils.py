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

# 3rd party
from decorating.animation import AnimatedDecorator
from requests.exceptions import ConnectionError

# self-package
from mal import color


class Unbuffered(object):

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


class StopSpinner(object):
    done = False
    position = 0
    message = 'loading'


# global variables from hell
sys.stdout = Unbuffered(sys.stdout)
sig = StopSpinner()


def killed():
    """Show a message if user terminated the program."""
    message = ("\n ┑(￣Д ￣)┍ somebody seems killed me..."
               "\nw a s  Y O U ?! ︵ヽ(`Д´)ﾉ︵﻿ ")
    print(color.colorize(message, 'red'), file=sys.stderr)
    os._exit(1)


def print_error(error_name, status, reason):
    padding = (len(error_name) + 2) * ' '
    error = color.colorize(error_name, 'red', 'bold')
    status = color.colorize(status, 'cyan')
    print(('{error}: {status}\n'
           '{padding}{reason} ¯\_(ツ)_/¯'.format_map(locals())),
          file=sys.stderr)


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
    @wraps(func) # keeps the wrapped function's name and docstring intact
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except BadRegexError:
            if AnimatedDecorator.controller.running:
                AnimatedDecorator.stop_animation()
            print_error('BadRegexError', 'invalid regex', 'reason: you')
            sys.exit(1)

        return result
    return wrapper


def checked_connection(func):
    """Wrap the function in a try/except to catch and handle a ConnectionError."""
    @wraps(func) # keeps the wrapped function's name and docstring intact
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except ConnectionError as e:
            if AnimatedDecorator.controller.running:
                AnimatedDecorator.stop_animation()
            err = e.args[0].args
            status, reason = err[0], err[1].args[1]
            error_name = e.__class__.__name__
            print_error(error_name, status, reason)
            sys.exit(1)
        return result

    return wrapper
