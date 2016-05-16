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
from mal.utils import usage, killed
from mal import login
from mal import color

signal.signal(signal.SIGINT, lambda x, y: killed())


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
    else:
        print("No matches in list 😢")
        return

    episode = item['episode'] + inc
    entry = {'episode': episode}
    if inc >= 1:
        procedure = 'Incrementing'
        procedure_color = 'green'
    else:
        procedure = 'Decrementing'
        procedure_color = 'red'

    template = {
        'title': color.colorize(item['title'], 'yellow', 'bold'),
        'episode': color.colorize(episode, 'red' if inc < 1 else 'green'),
        'total_episodes': color.colorize(item['total_episodes'], 'cyan'),
        'procedure': color.colorize(procedure, procedure_color)
    }

    print(('{procedure} progress for {title} to '
           '{episode}/{total_episodes}'.format_map(template)))

    if item['total_episodes'] == episode:
        entry['status'] = MyAnimeList.status_codes['completed']
        entry['date_finish'] = today
        print('Series completed!')
        score = int(input('Enter a score (or 0 for no score): '))
        if score != 0:
            entry['score'] = score
    elif episode == 1:
        entry['status'] = MyAnimeList.status_codes['watching']
        entry['date_start'] = datetime.date.today().strftime('%m%d%Y')

    response = mal.update(item['id'], entry)
    if response != 200:
        print("Failed with HTTP " + str(response))


def find(regex, filtering='all'):
    items = mal.find(regex)
    if len(items) == 0:
        print(color.colorize("No matches in list 😢", 'red', 'bold'))
        return

    if filtering != 'all':
        items = [x for x in items if x['status_name'] == filtering]

    n_items = color.colorize(str(len(items)), 'cyan', 'underline')
    print("Matched {} items:".format(n_items))

    sorted_items = sorted(items, key=itemgetter('status'), reverse=True)
    for index, item in enumerate(sorted_items):
        anime_pretty_print(index + 1, item)


def anime_pretty_print(index, item):
    padding = int(math.log10(index)) + 3
    remaining_color = ('blue' if item['episode'] < item['total_episodes']
                       else 'green')
    remaining = '{episode}/{total_episodes}'.format_map(item)
    in_rewatching = ('#in-rewatching-{rewatching}'.format_map(item)
                     if item['rewatching'] else '')
    template = {
        'index': index,
        'padding': ' ' * padding,
        'status': mal.status_names[item['status']].capitalize(),
        'title': color.colorize(item['title'], 'red', 'bold'),
        'remaining': color.colorize(remaining, remaining_color, 'bold'),
        'score': color.score_color(item['score']),
        'rewatching': (color.colorize(in_rewatching, 'yellow', 'bold'))
    }

    message_lines = [
        "{index}: {title}".format_map(template),
        ("{padding}{status} at {remaining} episodes "
         "with score {score} {rewatching}\n".format_map(template)),
    ]

    print('\n'.join(message_lines))


def main():
    global mal
    if not sys.stdout.isatty():
        color.COLORED = False
    args = sys.argv[1:]

    if not any(args):
        usage()

    if 'login' in args:
        login.create_credentials()
        sys.exit(0)

    config = login.get_credentials()
    mal = MyAnimeList.login(config)
    if not mal:
        print(color.colorize('Invalid credentials! :(', 'red', 'bold'))
        print(color.colorize('Tip: Try "mal login" again :D', 'white', 'bold'))
        sys.exit(1)

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
        else:
            find(args[0])


if __name__ == '__main__':
    main()
