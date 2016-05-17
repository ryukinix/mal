#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyleft © Manoel Vilela
#
#

import sys
import mal
import time
import os
import threading
from math import sin
from itertools import cycle
from functools import wraps
from sre_constants import error as BadRegexError

from requests.exceptions import ConnectionError
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


def usage():
    usage_info = [
        (("Usage: mal [inc/+1 | dec/-1] anime-by-regex\n"
          "       mal [watching | plan to watch | ... | rewatching]\n"
          "       mal [list | all]\n"
          "       mal anime-by-regex\n")),
        (("Ex. for increment +1:\n\n\t"
          "$ mal +1 lain\n")),
        (("Ex. for decrement -1:\n\n\t"
          "$ mal -1 lain\n")),
        (("Ex. filtering for section:\n\n\t"
          "$ mal watching\n")),
        (("Ex. search return all anime whose start with s: \n\n\t"
          "$ mal ^s\n")),
        (("Ex. fetch all list: \n\n\t"
          "$ mal list\n\t"
          "$ mal all\n\t"
          "$ mal .+\n")),
        "Hacked by {__author__} <{__email__}> | "
        "version {__version__}".format_map(vars(mal)),
    ]
    print('\n'.join(usage_info), file=sys.stderr)
    sys.exit(1)


def killed():
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

animation_diagram = "⣾⣽⣻⢿⡿⣟⣯"
animation_spinner = '▁▂▃▄▅▆▇▆▅▄▃▁'


def spinner(control):
    animation = ''.join(x * 5 for x in animation_diagram)
    if not sys.stdout.isatty():  # not send to pipe/redirection
        return
    anim = zip(cycle(animation), cycle(animation_spinner))
    for n, start_end_anim in enumerate(anim):
        start, end = start_end_anim
        padding = '█' * int(20 * abs(sin(0.05 * (n + control.position))))
        padding_colored = color.colorize(padding, 'cyan')
        banner = '{} {} {}'.format(start, control.message, end)
        banner_colored = color.colorize(banner, 'cyan')
        message = '\r' + padding_colored + banner_colored
        sys.stdout.write(message)
        time.sleep(0.05)
        sys.stdout.write('\r' + len(message) * ' ')
        sys.stdout.write(2 * len(message) * "\010")
        if control.done:
            control.position = n
            break
    sys.stdout.write(len(message) * ' ')
    sys.stdout.write('\r' + 2 * len(message) * "\010")

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


# deal with it
def animated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global last_thread
        if not wrapper.running:
            sig.message = func.__name__
            spinner_thread = threading.Thread(target=spinner, args=(sig,))
            spinner_thread.start()
            last_thread = spinner_thread
            wrapper.running = True
        result = func(*args, **kwargs)
        if wrapper.running:
            sig.done = True
            spinner_thread.join()
            wrapper.running = False
            sig.done = False

        return result

    wrapper.running = False

    return wrapper

# END OF THE LOL ZONE


def checked_regex(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except BadRegexError:
            print_error('BadRegexError', 'invalid regex', 'reason: you')
            os._exit(1)

        return result
    return wrapper


def checked_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except ConnectionError as e:
            if 'last_thread' in globals():
                sig.done = True
                last_thread.join()
            err = e.args[0].args
            status, reason = err[0], err[1].args[1]
            error_name = e.__class__.__name__
            print_error(error_name, status, reason)
            os._exit(1)
        return result

    return wrapper
