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
from requests.exceptions import ConnectionError
from functools import wraps
from mal import color


def usage():
    usage_info = [
        (("Usage: mal [inc/+1 | dec/-1] anime-by-regex\n"
          "       mal [watching | plan to watch | ... | rewatching]\n"
          "       mal [list | all]\n"
          "       mal anime-by-regex\n")),
        (("Ex. for increment +1:\n\n\t"
          "$ mal +1 'samurai champloo'\n")),
        (("Ex. for decrement -1:\n\n\t"
          "$ mal -1 'samurai champloo'\n")),
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
    print('\n'.join(usage_info))
    sys.exit(1)


def killed():
    print("\nD: somebody killed me...")
    sys.exit(1)


def checked_connection(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except ConnectionError as e:
            err = e.args[0].args
            status, reason = err[0], err[1].args[1]
            error_name = e.__class__.__name__
            padding = (len(error_name) + 2) * ' '
            error = color.colorize(error_name, 'red', 'bold')
            status = color.colorize(status, 'cyan')
            print('{error}: {status}\n{padding}{reason}'.format_map(locals()))
            sys.exit(1)

        return result

    return wrapper
