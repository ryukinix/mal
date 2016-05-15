#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyleft © Manoel Vilela
#
#

# stdlib
import sys
import signal
import datetime
import math
from operator import itemgetter

# self-package
from mal.api import MyAnimeList
from mal.utils import colorize, score_color, usage, killed
from mal import login

signal.signal(signal.SIGINT, lambda x, y: killed())
today = datetime.date.today().strftime('%m%d%Y')


def isomorphic_increment(aliases, arguments):
    command = (aliases & set(arguments)).pop()
    return arguments[arguments.index(command) - len(arguments[1:])]


def increment(regex, inc):
    items = mal.find(regex)
    item = None

    for index, i in reversed(list(enumerate(items))):
        if i['status'] == MyAnimeList.status_codes['completed']:
            del items[index]

    if len(items) > 1:
        print('Multiple results:')
        for index, title in enumerate(map(itemgetter('title'), items)):
            print('{index}: {title}'.format_map(locals()))
        index = int(input('Which one? '))
        item = items[index]

    elif len(items) == 1:
        item = items[0]

    if not item:
        print("No matches in list 😢")
        return

    episode = item['episode'] + inc
    entry = {'episode': episode}

    template = {
        'title': colorize(item['title'], 'yellow', 'bold'),
        'episode': colorize(str(episode), 'red' if inc < 1 else 'green'),
        'total_episodes': colorize(item['total_episodes'], 'cyan'),
        'procedure': colorize('Incrementing', 'green') if inc >= 1 else colorize('Decrementing', 'red')
    }

    print(('{procedure} progress for '
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
        print(colorize("No matches in list.", 'red', 'bold'))
        return

    if filtering != 'all':
        items = [x for x in items if x['status_name'] == filtering]

    n_items = colorize(str(len(items)), 'cyan', 'underline')
    print("Matched {} items:".format(n_items))

    sorted_items = sorted(items, key=itemgetter('status'), reverse=True)
    for index, item in enumerate(sorted_items):
        if index == 0:
            padding = 3
        else:
            padding = int(math.log10(index)) + 3
        template = {
            'index': index + 1,
            'title': colorize(item['title'], 'red', 'bold'),
            'padding': ' ' * padding,
            'status': mal.status_names[item['status']].capitalize(),
            'remaining': colorize(
                '{episode}/{total_episodes}'.format_map(item),
                'blue' if item['episode'] < item['total_episodes']
                       else 'green',
                'bold'),
            'score': score_color(item['score']),
            'rewatching': (colorize('#in-rewatching-{}'.format(item['rewatching']), 'yellow', 'bold')
                           if item['rewatching'] else '')
        }

        print("{index}: {title}".format_map(template))
        print("{padding}{status} at {remaining} episodes "
              "with score {score} {rewatching}".format_map(template))
        print()


def main():
    global mal
    config = login.get_credentials()
    mal = MyAnimeList(config)

    args = sys.argv[1:]

    subcommand_splitted = ' '.join(map(str.lower, args))
    if subcommand_splitted in mal.status_names.values():
        args = [subcommand_splitted]
    if 3 > len(args) > 1:
        if any(x in args for x in ('inc', '+1')):
            query = isomorphic_increment({'inc', '+1'}, args)
            increment(query, 1)
        elif any(x in args for x in ('dec', '-1')):
            query = isomorphic_increment({'dec', '-1'}, args)
            increment(query, -1)
        else:
            print('subcommand not supported. 😢')
    elif len(args) == 1:
        if args[0].lower() in mal.status_names.values():
            find('.+', args[0].lower())
        elif args[0] in ('all', 'list'):
            find('.+')
        elif args[0] == 'login':
            login.create_credentials()
        else:
            find(args[0])

    else:
        usage()


if __name__ == '__main__':
    main()
