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
from mal import setup


def search(mal, args):
    """Search MAL (not just the user) anime database."""
    core.search(mal, args.anime_title.lower(), full=args.extend)


def filter(mal, args):
    """Search and find an anime in the users list."""
    core.find(mal, args.anime_regex.lower(), extra=args.extend, user=args.user)


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
    core.find(mal, '.+', args.section, extra=args.extend, user=args.user)


def drop(mal, args):
    """Drop a anime from lists based in a regex expression"""
    core.drop(mal, args.anime_regex)


def stats(mal, args):
    """Show the users anime watching statistics as presented on MAL."""
    core.stats(mal, args.user)


def add(mal, args):
    """Add an anime with a certain status to the list."""
    core.add(mal, args.anime_regex.lower(), status=args.status)


def config(mal, args):
    # Show the current config file
    setup.print_config()


def edit(mal, args):
    """Edit an entry in the users list, if it was present. Notify otherwise."""
    changes = dict()
    for field in ['score', 'status', 'tags', 'add_tags']:
        attr = getattr(args, field)
        if attr is not None:
            changes[field] = attr

    # turn list of tags into a single string if needed
    for field in ['tags', 'add_tags']:
        if field in changes.keys():
            changes[field] = ' '.join(changes[field])

    core.edit(mal, args.anime_regex.lower(), changes)
