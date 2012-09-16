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


def increment(regex):
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

    if item == None:
        print("No matches in list.")
        return

    episode = item['episode'] + 1
    entry = {'episode': episode}

    print('Incrementing progress for ' + item['title'] + ' to ' + str(episode))

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
        print ("Failed with HTTP " + str(response))


def find(regex):
    items = mal.find(regex)
    if len(items) == 0:
        print("No matches in list.")
        return

    print("Matched " + str(len(items)) + " items:")

    for index, item in enumerate(items):
        if index == 0:
            padding = 3
        else:
            padding = int(math.log10(index)) + 3

        status = MyAnimeList.status_names[item['status']].capitalize()

        print(str(index) + ': ' + item['title'])
        print(' ' * padding + status + ' at ' + str(item['episode']) +
              '/' + str(item['total_episodes']) + ' episodes')
        print()


config = ConfigParser()
config.read(os.path.expanduser('~/.myanimelist.ini'))

mal = MyAnimeList(config['mal'])

args = sys.argv[1:]

if len(args) > 1:
    if args[0] == 'inc':
        increment(args[1])

elif len(args) == 1:
    find(args[0])

else:
    print("Usage: mal [command] regex")
    print("Real help coming eventually.")
