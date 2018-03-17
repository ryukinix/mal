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
import signal
import argparse

# self-package
import mal
from mal.api import MyAnimeList
from mal.utils import killed
from mal import color
from mal import login
from mal import commands
from mal import setup

import decorating

# catch if the user presses Ctrl+c and exit a special message
signal.signal(signal.SIGINT, lambda x, y: killed())


def create_parser():
    parser = argparse.ArgumentParser(prog='mal',
                                     description='MyAnimeList command line client.')
    parser.add_argument('-v',
                        '--version',
                        action='store_true',
                        help='show the version of mal')
    subparsers = parser.add_subparsers(help='commands', dest='command')

    # Parser for "search" command
    parser_search = subparsers.add_parser('search',
                                          help='search an anime globally on MAL')
    parser_search.add_argument('anime_title',
                               help='a substring to match anime titles')
    parser_search.add_argument('--extend', action='store_true', # defaults to false
                               help='display all available information on anime')
    parser_search.set_defaults(func=commands.search)

    # Parser for "filter" command
    parser_filter = subparsers.add_parser('filter',
                                          help='find anime in users list')
    parser_filter.add_argument('anime_regex',
                               help='regex pattern to match anime titles')
    parser_filter.add_argument('--extend', action='store_true',
                               help='display all available information on anime')
    parser_filter.add_argument('--user', type=str, default=None,
                              help='choose which users list to filter through')
    parser_filter.set_defaults(func=commands.filter)

    # Parser for "increase" command
    parser_increase = subparsers.add_parser('increase',
                                            help="increase anime's watched episodes by one",
                                            aliases=['inc'])
    parser_increase.add_argument('anime_regex',
                                 help='regex pattern to match anime titles')
    parser_increase.add_argument('episodes',
                                 nargs='?',
                                 type=int,
                                 default=1,
                                 help='number of episodes to increase')
    parser_increase.set_defaults(func=commands.increase)

    # Parser for "decrease" command
    parser_decrease = subparsers.add_parser('decrease',
                                            help="decrease anime's watched episodes by one",
                                            aliases=['dec'])
    parser_decrease.add_argument('anime_regex',
                                  help='regex pattern to match anime titles')
    parser_decrease.add_argument('episodes',
                                 nargs='?',
                                 type=int,
                                 default=1,
                                 help='number of episodes to decrease')

    parser_decrease.set_defaults(func=commands.decrease)

    # Parser for "login" command
    parser_login = subparsers.add_parser('login',
                                          help='save login credentials')
    parser_login.set_defaults(func=commands.login)

    # Parser for "list" command
    parser_list = subparsers.add_parser('list', help='list animes')
    parser_list.add_argument('section',
                             help=('section to display, can be one of: '
                                   '[%(choices)s] (default: %(default)s)'),
                             nargs='?',
                             default='all',
                             metavar='section',
                             choices=['all', 'watching', 'completed',
                                      'on hold', 'dropped',
                                      'plan to watch', 'rewatching'])
    parser_list.add_argument('--extend', action='store_true', # defaults to False
                             help='display extra info such as start/finish dates and tags')
    parser_list.add_argument('--user', type=str, default=None,
                              help='choose which users list to show')
    parser_list.set_defaults(func=commands.list)

    # Parser for "config" command
    parser_config = subparsers.add_parser('config',
                                          help='Print current config file and its path')
    parser_config.set_defaults(func=commands.config)

    # Parser for "drop" command
    parser_drop = subparsers.add_parser('drop',
                                        help='Put a selected anime on drop list')
    parser_drop.add_argument('anime_regex',
                             help='regex pattern to match anime titles')
    parser_drop.set_defaults(func=commands.drop)

    # Parser for "stats" command
    parser_stats = subparsers.add_parser('stats',
                                         help='Show anime watch stats')
    parser_stats.add_argument('--user', type=str, default=None,
                              help='which users list to pull stats from')
    parser_stats.set_defaults(func=commands.stats)

    # Parser for "add" command
    parser_add = subparsers.add_parser('add',
                                      help='add an anime to the list')
    parser_add.add_argument('anime_regex',
                            help='regex pattern to match anime titles')
    parser_add.add_argument('status', type=str, nargs='?',
                            default="plan to watch",
                            help='add anime with this status (e.g "on hold")')
    parser_add.set_defaults(func=commands.add)

    # Parser for "edit" command
    parser_edit = subparsers.add_parser('edit',
                                        help='edit entry')
    parser_edit.add_argument('anime_regex',
                             help='regex pattern to match anime titles')
    parser_edit.add_argument('--score', type=int)
    parser_edit.add_argument('--status',
                             help='status to assign to entry',
                             choices=['watching', 'completed',
                                      'on hold', 'dropped',
                                      'plan to watch', 'rewatching'])
    parser_edit_tags = parser_edit.add_mutually_exclusive_group()
    parser_edit_tags.add_argument('--set-tags', nargs='+', metavar='tag',
                                  dest='tags',
                                  help=('space separated list of tags'
                                        ' (replaces current tags)'))
    parser_edit_tags.add_argument('--add-tags', nargs='+', metavar='tag',
                                  help='add these tags to the current ones')
    parser_edit.set_defaults(func=commands.edit)

    return parser


def main():
    parser = create_parser()
    # Parse arguments
    if len(sys.argv) <= 1:
        args = parser.parse_args(['-h'])
    else:
        args = parser.parse_args()

    if args.version:
        print(mal.__version__)
        sys.exit(0)

    # if the command is login, create credentials and exits
    # NOTE: if this statement is removed the `mal login` and
    # no credentials exists, login.create_credentials() will
    # be called twice! On login.get_credentials and args.func(mal, args)
    if args.command == 'login':
        login.create_credentials()
        sys.exit(0)

    # Check if authorized
    config = login.get_credentials()
    if config['config']['animation'].lower() == 'false':
        decorating.animated.enabled = False

    mal_api = MyAnimeList.login(config)
    if not mal_api:
        print(color.colorize('Invalid credentials! :(', 'red', 'bold'))
        print(color.colorize('Tip: Try "mal login" again :D', 'white', 'bold'))
        sys.exit(1)

    # Execute sub command
    args.func(mal_api, args)


if __name__ == '__main__':
    main()
