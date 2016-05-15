#!/usr/bin/env python

import sys
import os
import signal
import datetime
import math
from configparser import ConfigParser
from myanimelist import MyAnimeList


signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
today = datetime.date.today().strftime('%m%d%Y')


color_map = {
    'red': '\033[01;31m',
    'cyan': '\033[01;36m',
    'blue': '\033[01;34m',
    'green': '\033[01;32m',
    'reset': '\033[00m'
}


def colorize(string, color):
    color_selected = color_map[color]
    reset = color_map['reset']
    return '{color_selected}{string}{reset}'.format_map(locals())


def increment(regex, inc):
    items = mal.find(regex)
    item = None

    for index, i in reversed(list(enumerate(items))):
        if i['status'] == MyAnimeList.status_codes['completed']:
            del items[index]

    if len(items) > 1:
        print('Multiple results:')
        for index, item in enumerate(items):
            print(str(index) + ': ' + item['title'])
        index = int(input('Which one? '))
        item = items[index]

    elif len(items) == 1:
        item = items[0]

    if item is None:
        print("No matches in list.")
        return

    episode = item['episode'] + inc
    entry = {'episode': episode}

    template = {
        'title': colorize(item['title'], 'cyan'),
        'episode': colorize(str(episode), 'red' if inc < 1 else 'green'),
        'total_episodes': colorize(item['total_episodes'], 'blue')
    }

    print(('Incrementing progress for '
           '{title} to {episode}/{total_episodes}'.format_map(template)))  # noqa

    if item['total_episodes'] == episode:
        entry['status'] = MyAnimeList.status_codes['completed']
        entry['date_finish'] = today
        print('Series completed!')
        score = int(input('Enter a score (or 0 for no score): '))
        if score != 0:
            entry['score'] = score
    elif episode == 1:
        entry['status'] = MyAnimeList.status_codes['watching']
        entry['date_start'] = today

    response = mal.update(item['id'], entry)
    if response != 200:
        print("Failed with HTTP " + str(response))


def find(regex):
    items = mal.find(regex)
    if len(items) == 0:
        print("No matches in list.")
        return

    print("Matched " + colorize(str(len(items)), 'cyan') + " items:")

    for index, item in enumerate(items):
        if index == 0:
            padding = 3
        else:
            padding = int(math.log10(index)) + 3

        status = MyAnimeList.status_names[item['status']].capitalize()
        title = colorize(item['title'], 'red')
        print(str(index + 1) + ': ' + '{}'.format(title))  # noqa
        print(' ' * padding + status + ' at ' + str(item['episode']) +
              '/' + str(item['total_episodes']) + ' episodes')
        print()

if __name__ == '__main__':
    config = ConfigParser()
    config.read(os.path.expanduser('~/.myanimelist.ini'))
    mal = MyAnimeList(config['mal'])

    args = sys.argv[1:]

    if len(args) > 1:
        if 'inc' in args:
            increment(args[args.index('inc') - len(args[1:])], 1)
        elif 'dec' in args:
            increment(args[args.index('dec') - len(args[1:])], -1)

    elif len(args) == 1:
        find(args[0])

    else:
        print("Usage: mal [inc | dec] anime-by-regex")
        print("Hacked by Manoel Vilela")
        print("Ex.: mal inc 'samurai champloo'")
