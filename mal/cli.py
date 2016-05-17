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
import math
from operator import itemgetter
from datetime import date

# self-package
from mal.api import MyAnimeList
from mal.utils import usage, killed
from mal import login
from mal import color

signal.signal(signal.SIGINT, lambda x, y: killed())


# creep mode activated
# '$ mal +1 anime' <-> '$ mal anime +1'
# where +1 is a alias inside of set aliases.
def isomorphic_increment(aliases, arguments):
    command = (aliases & set(arguments)).pop()
    return arguments[arguments.index(command) - len(arguments[1:])]


def select_item(items):
    item = None
    if len(items) > 1:
        print(color.colorize('Multiple results:', 'cyan'))
        for index, title in enumerate(map(itemgetter('title'), items)):
            print('{index}: {title}'.format_map(locals()))
        index = int(input('Which one? '))
        item = items[index]
    elif len(items) == 1:
        item = items[0]
    else:
        print(color.colorize("No matches in list ᕙ(⇀‸↼‶)ᕗ", 'red'))
        sys.exit(1)

    return item


def start_end(entry, episode, total_episodes):
    if total_episodes == episode:
        entry['status'] = MyAnimeList.status_codes['completed']
        entry['date_finish'] = date.today().strftime('%m%d%Y')
        print(color.colorize('Series completed!', 'green'))
        score = int(input('Enter a score (or 0 for no score): '))
        if score != 0:
            entry['score'] = score
    elif episode == 1:
        entry['status'] = MyAnimeList.status_codes['watching']
        entry['date_start'] = date.today().strftime('%m%d%Y')

    return entry


def remove_completed(items):
    # remove animes whose is already completed
    # preserves (rewatching)
    for index, status in enumerate(map(itemgetter('status_name'), items)):
        if status == 'completed':
            del items[index]

    return items


def progress_update(mal, regex, inc):
    items = remove_completed(mal.find(regex))
    item = select_item(items)
    episode = item['episode'] + inc
    entry = dict(episode=episode)
    template = {
        'title': color.colorize(item['title'], 'yellow', 'bold'),
        'episode': color.colorize(episode, 'red' if inc < 1 else 'green'),
        'total_episodes': color.colorize(item['total_episodes'], 'cyan'),
        'procedure': color.procedure_color(inc)
    }

    print(('{procedure} progress for {title} to '
           '{episode}/{total_episodes}'.format_map(template)))

    entry = start_end(entry, episode, item['total_episodes'])
    response = mal.update(item['id'], entry)
    if response != 200:
        print(color.colorize("Failed with HTTP: {}".format(response), 'red'))


def find(mal, regex, filtering='all'):
    items = mal.find(regex)
    if len(items) == 0:
        print(color.colorize("No matches in list ᕙ(⇀‸↼‶)ᕗ", 'red'))
        return

    if filtering != 'all':
        items = [x for x in items if x['status_name'] == filtering]

    n_items = color.colorize(str(len(items)), 'cyan', 'underline')
    print("Matched {} items:".format(n_items))

    sorted_items = sorted(items, key=itemgetter('status'), reverse=True)
    for index, item in enumerate(sorted_items):
        anime_pprint(index + 1, item)


def anime_pprint(index, item):
    padding = int(math.log10(index)) + 3
    remaining_color = ('blue' if item['episode'] < item['total_episodes']
                       else 'green')
    remaining = '{episode}/{total_episodes}'.format_map(item)
    in_rewatching = ('#in-rewatching-{rewatching}'.format_map(item)
                     if item['rewatching'] else '')
    template = {
        'index': index,
        'padding': ' ' * padding,
        'status': MyAnimeList.status_names[item['status']].capitalize(),
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


# parsing -> '$ mal on hold' -> '# mal "on hold"''
def filtering_splitted(args):
    subcommand_splitted = ' '.join(map(str.lower, args))
    if subcommand_splitted in MyAnimeList.status_names.values():
        args = [subcommand_splitted]

    return args


def commands(mal, args):
    if 3 > len(args) > 1:
        if any(x in args for x in ('inc', '+1')):
            query = isomorphic_increment({'inc', '+1'}, args)
            progress_update(mal, query, 1)
        elif any(x in args for x in ('dec', '-1')):
            query = isomorphic_increment({'dec', '-1'}, args)
            progress_update(mal, query, -1)
        else:
            print('subcommand not supported. ᕙ(⇀‸↼‶)ᕗ')
    elif len(args) == 1:
        if args[0].lower() in mal.status_names.values():
            find(mal, '.+', args[0].lower())
        elif args[0] in ('all', 'list'):
            find(mal, '.+')
        else:
            find(mal, args[0])


def main():
    if not sys.stdout.isatty():
        color.COLORED = False
    args = sys.argv[1:]

    if not any(args) or any(x in args for x in ('-h', '--help', 'help')):
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

    args = filtering_splitted(args)
    commands(mal, args)


if __name__ == '__main__':
    main()
