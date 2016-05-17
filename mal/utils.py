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

from requests.exceptions import ConnectionError
from mal import color


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


animation_diagram = "⣾⣽⣻⢿⡿⣟⣯"
animation_spinner = '▁▂▃▄▅▆▇▆▅▄▃▁'

#    /\O    |    _O    |      O
#     /\/   |   //|_   |     /_
#    /\     |    |     |     |\
#   /  \    |   /|     |    / |
# LOL  LOL  |   LLOL   |  LOLLOL


def spinner(control):
    animation = ''.join(x * 2 for x in animation_spinner)
    if not sys.stdout.isatty():  # not send to pipe/redirection
        return
    anim = zip(cycle(animation), cycle(reversed(animation)))
    for n, start_end_anim in enumerate(anim):
        start, end = start_end_anim
        padding = '█' * int(20 * abs(sin(0.05 * (n + control.position))))
        padding_colored = color.colorize(padding, 'cyan')
        banner = color.colorize(start + " loading data " + end, 'cyan')
        message = '\r' + padding_colored + banner
        sys.stdout.write(message)
        time.sleep(0.03)
        sys.stdout.write('\r' + len(message) * ' ')
        sys.stdout.write(2 * len(message) * "\010")
        sys.stdout.flush()
        if control.done:
            control.position = n
            break
    sys.stdout.write(len(message) * ' ')
    sys.stdout.write('\r' + 2 * len(message) * "\010")
    sys.stdout.flush()


class Unbuffered(object):

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


sys.stdout = Unbuffered(sys.stdout)


class StopSpinner:
    done = False
    position = 0

sig = StopSpinner()


def killed():
    message = ("\n ┑(￣Д ￣)┍ somebody seems killed me..."    
               "\nw a s  Y O U ?! ︵ヽ(`Д´)ﾉ︵﻿ ")
    print(color.colorize(message, 'red'), file=sys.stderr)
    os._exit(1)


# deal with it
def spinnered(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global last_thread
        if not wrapper.running:
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


def checked_connection(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except ConnectionError as e:
            err = e.args[0].args
            status, reason = err[0], err[1].args[1]
            error_name = e.__class__.__name__
            padding = (len(error_name) + 2) * ' '
            error = color.colorize(error_name, 'red', 'bold')
            status = color.colorize(status, 'cyan')
            sig.done = True
            last_thread.join()
            print('{error}: {status}\n{padding}{reason} ¯\_(ツ)_/¯'.format_map(locals()),
                  file=sys.stderr)
            os._exit(1)

        return result

    return wrapper
