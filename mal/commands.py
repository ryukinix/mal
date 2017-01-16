#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#
"""These function serve as an entry point for the several subcommands
of mal. All they do is basically call the functions that do actual work
in the core module."""

# stdlib
import sys

# self-package
from mal import core
from mal import login as _login


def search(mal, args):
    """Search MAL (not just the user) anime database."""
    core.find(mal, args.anime_regex.lower())


def increase(mal, args):
    core.progress_update(mal, args.anime_regex.lower(), args.episodes)


def decrease(mal, args):
    core.progress_update(mal, args.anime_regex.lower(), -args.episodes)


def login(mal, args):
    """Creates login credentials so that next time the program is called
    it can log in right at the start without any problem."""
    _login.create_credentials()
    sys.exit(0)


def list(mal, args):
    """Show all the animes on the users list."""
    # . matches any character except line breaks
    # + matches one or more occurences of the previous character
    if (args.section == 'all'):
        core.find(mal, '.+')
    else:
        core.find(mal, '.+', args.section)


def config(mal, args):
    # TODO implement config command
    print("config - not implemented yet")


def download(mal, args):
    # TODO implement download command
    print("download - not implemented yet")


def watch(mal, args):
    # TODO implement watch command
    print("watch - not implemented yet")
