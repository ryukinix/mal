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

# self-package
from mal import core
from mal import login as _login

def search(mal, args):
    core.find(mal, vars(args)['anime-regex'].lower())


def increase(mal, args):
    core.progress_update(mal, vars(args)['anime-regex'].lower(), 1)


def decrease(mal, args):
    core.progress_update(mal, vars(args)['anime-regex'].lower(), -1)


def login(mal, args):
    _login.create_credentials()
    sys.exit(0)


def list(mal, args):
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