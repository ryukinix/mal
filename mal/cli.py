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
from mal.api import MyAnimeList
from mal.utils import killed
from mal import color
from mal import login
from mal import commands

# catch if the user presses Ctrl+c and exit a special message
signal.signal(signal.SIGINT, lambda x, y: killed())


def create_parser():
    parser = argparse.ArgumentParser(prog='mal',
                                     description='MyAnimeList command line client.')
    subparsers = parser.add_subparsers(help='commands')

    # Parser for "search" command
    parser_search = subparsers.add_parser('search',
                                          help='search an anime')
    parser_search.add_argument('anime_regex',
                               help='regex pattern to match anime titles')
    parser_search.set_defaults(func=commands.search)

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
    parser_search = subparsers.add_parser('login',
                                          help='save login credentials')
    parser_search.set_defaults(func=commands.login)

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
    parser_list.set_defaults(func=commands.list)

    # Parser for "config" command
    parser_config = subparsers.add_parser('config',
                                          help='config - not implemented yet')
    parser_config.set_defaults(func=commands.config)

    # Parser for "download" command
    parser_download = subparsers.add_parser('download',
                                            help='download - not implemented yet')
    parser_download.set_defaults(func=commands.download)

    # Parser for "watch" command
    parser_watch = subparsers.add_parser('watch',
                                         help='watch - not implemented yet')
    parser_watch.set_defaults(func=commands.watch)

    return parser


def main():
    parser = create_parser()
    # Parse arguments
    if len(sys.argv) <= 1:
        args = parser.parse_args(['-h'])
    else:
        args = parser.parse_args()

    # Check if authorized
    config = login.get_credentials()
    mal = MyAnimeList.login(config)
    if not mal:
        print(color.colorize('Invalid credentials! :(', 'red', 'bold'))
        print(color.colorize('Tip: Try "mal login" again :D', 'white', 'bold'))
        sys.exit(1)

    # Execute sub command
    args.func(mal, args)


if __name__ == '__main__':
    main()
