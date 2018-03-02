#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

# 3rd party
from decorating.color import colorize


def score_color(score):
    """Choose color of output based on how high the score is."""
    if score == 10:
        return colorize(score, 'green', 'bold')
    if score >= 9:
        return colorize(score, 'cyan', 'bold')
    elif score >= 7:
        return colorize(score, 'blue', 'bold')
    elif score >= 5:
        return colorize(score, 'yellow', 'bold')
    elif score >= 1:
        return colorize(score, 'red', 'bold')
    else:
        return colorize('-', 'pink', 'bold')


def procedure_color(increment):
    """Choose output color when incrementing/decrementing."""
    if increment >= 1:
        procedure = 'Incrementing'
        procedure_color = 'green'
    else:
        procedure = 'Decrementing'
        procedure_color = 'red'
    return colorize(procedure, procedure_color)
