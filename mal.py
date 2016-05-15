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
    'brown'  : '\033[{style};30m',
    'red'    : '\033[{style};31m',
    'green'  : '\033[{style};32m',
    'yellow' : '\033[{style};33m',
    'blue'   : '\033[{style};34m',
    'pink'   : '\033[{style};35m',
    'cyan'   : '\033[{style};36m',
    'gray'   : '\033[{style};37m',
    'reset'  : '\033[00;00m'
}

style_map = {
    'normal'    : '00',
    'bold'      : '01',
    'underline' : '04',
}


def colorize(string, color_selected, style_selected='normal'):
    style = style_map[style_selected]
    color = color_map[color_selected].format(style=style)
    reset = color_map['reset']
    return '{color}{string}{reset}'.format_map(locals())


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
        'title': colorize(item['title'], 'cyan', 'underline'),
        'episode': colorize(str(episode), 'red' if inc < 1 else 'green'),
        'total_episodes': colorize(item['total_episodes'], 'yellow')
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


def find(regex, filtering='all'):
    items = mal.find(regex)
    if len(items) == 0:
        print("No matches in list.")
        return
    if filtering != 'all':
        items = list(filter(lambda x: mal.get_status_name(x['status']) == filtering, items))

    print("Matched " + colorize(str(len(items)), 'cyan', 'underline') + " items:")

    sorted_items = sorted(items, key=lambda x: mal.get_status_name(x['status']))
    for index, item in enumerate(sorted_items):
        if index == 0:
            padding = 3
        else:
            padding = int(math.log10(index)) + 3

        status = mal.status_names[item['status']].capitalize()
        title = colorize(item['title'], 'red', 'bold')
        remaining = colorize('{episode}/{total_episodes}'.format_map(item), 
                    'blue' if item['episode'] < item['total_episodes'] else 'green', 'bold') 
        print(str(index + 1) + ': ' + '{}'.format(title))  # noqa
        print(' ' * padding + status + ' at ' + 
              remaining + ' episodes')
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
        else:
            print('subcommand not supported.')
    elif len(args) == 1:
        if args[0].lower() in mal.status_names.values():
            find('.+', args[0].lower())
        else:
            find(args[0])

    else:
        print("Usage: mal [inc | dec | filtering] anime-by-regex")
        print("Hacked by Manoel Vilela\n\n")
        print("Ex. for increment +1:\n\n\t $ mal inc 'samurai champloo'\n")
        print("Ex. for decrement -1:\n\n\t $ mal dec 'samurai champloo'\n")
        print("Ex. filtering:\n\n\t $ mal watching\n")
        print("Ex. search return all anime whose start with s:\n\n\t $ mal ^s\n")
