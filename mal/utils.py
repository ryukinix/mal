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

color_map = {
    'brown': '\033[{style};30m',
    'red': '\033[{style};31m',
    'green': '\033[{style};32m',
    'yellow': '\033[{style};33m',
    'blue': '\033[{style};34m',
    'pink': '\033[{style};35m',
    'cyan': '\033[{style};36m',
    'gray': '\033[{style};37m',
    'white': '\033[{style};40m',
    'reset': '\033[00;00m'
}

style_map = {
    'normal': '00',
    'bold': '01',
    'underline': '04',
}


def colorize(printable, color_selected, style_selected='normal'):
    style = style_map[style_selected]
    color = color_map[color_selected].format(style=style)
    reset = color_map['reset']
    return '{color}{printable}{reset}'.format_map(locals())


def score_color(score):
    if score == 10:
        return colorize(score, 'green', 'bold')
    if score >= 9:
        return colorize(score, 'cyan', 'bold')
    elif score >= 7:
        return colorize(score, 'blue', 'bold')
    elif score >= 5:
        return colorize(score, 'yellow', 'bold')
    elif score > 1:
        return colorize(score, 'red', 'bold')
    else:
        return colorize('undefined', 'pink', 'bold')


def usage():
    usage_info = [
        (("Usage: mal [inc | dec] anime-by-regex\n"
          "       mal [watching | plan to watch | on hold | completed | rewatching]\n"
          "       mal [list | all]\n"
          "       mal anime-by-regex\n")),
        (("Ex. for increment +1:\n\n\t"
          "$ mal inc 'samurai champloo'\n")),
        (("Ex. for decrement -1:\n\n\t"
          "$ mal dec 'samurai champloo'\n")),
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
    print("D: somebody killed me")
    sys.exit(1)
