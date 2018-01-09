#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

# stdlib
import os
import sys
import math
import html
import tempfile
import subprocess
from operator import itemgetter
from datetime import date

# self-package
from mal.api import MyAnimeList
from mal.utils import print_error
from mal import color


def report_if_fails(response):
    if response != 200:
        print(color.colorize("Failed with HTTP: {}".format(response), 'red'))


def select_item(items):
    """Select a single item from a list of results."""
    item = None
    if len(items) > 1:  # ambigious search results
        print(color.colorize('Multiple results:', 'cyan'))
        # show user the results and make them choose one
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
    """Fill details of anime if user just started it or finished it."""
    if total_episodes == episode:
        entry['status'] = MyAnimeList.status_codes['completed']
        entry['date_finish'] = date.today().strftime('%m%d%Y')
        print(color.colorize('Series completed!', 'green'))

        # set/change score
        user_score = input(
            'Enter new score (leave blank to keep score at {}): '.format(
            entry.get('score', 0))
        ).strip()
        if user_score: # do nothing if blank answer
            try:
                entry['score'] = int(user_score)
            except ValueError:
                print(color.colorize('Invalid score.', 'red'))

    elif episode == 1:
        entry['status'] = MyAnimeList.status_codes['watching']
        entry['date_start'] = date.today().strftime('%m%d%Y')

    return entry


def remove_completed(items):
    # remove animes that are already completed
    # preserves (rewatching)
    for index, status in enumerate(map(itemgetter('status_name'), items)):
        if status == 'completed':
            del items[index]

    return items


def progress_update(mal, regex, inc):
    items = remove_completed(mal.find(regex))
    item = select_item(items)  # also handles ambigious searches
    episode = item['episode'] + inc
    entry = dict(episode=episode, score=item.get('score', 0))
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
    report_if_fails(response)


def search(mal, regex, full=False):
    """Search the MAL database for an anime."""
    result = mal.search(regex)
    # if no results or only one was found we treat them special
    if len(result) == 0:
        print(color.colorize("No matches in MAL database ᕙ(⇀‸↼‶)ᕗ", 'red'))
        return
    if len(result) == 1: full = True # full info if only one anime was found

    lines = ["{index}: {title}", "  Episodes: {episodes}\tScore: {score}", "  Synopsis: {synopsis}"]
    extra_lines = ["  Start date: {start}\tEnd data: {end}", "  Status: {status}"]

    print("Found", color.colorize(str(len(result)), "cyan", "underline"), "animes:")
    for i, anime in enumerate(result):
        # replace tags and special html chars (like &mdash;) with actual characters
        synopsis = html.unescape(str(anime["synopsis"])).replace("<br />", "")
        if len(synopsis) > 70 and not full:
            synopsis = synopsis[:70] + "..."

        # this template/line stuff might need some refactoring
        template = {
            "index": str(i + 1),
            "title": color.colorize(anime["title"], "red", "bold"),
            "episodes": color.colorize(anime["episodes"], "white", "bold"),
            "score": color.score_color(float(anime["score"])),
            "synopsis": synopsis,
            "start": anime["start_date"] if anime["start_date"] != "0000-00-00" else "NA",
            "end": anime["end_date"] if anime["end_date"] != "0000-00-00" else "NA",
            "status": anime["status"]
        }
        print("\n".join(line.format_map(template) for line in lines))
        if full: print("\n".join(line.format_map(template) for line in extra_lines))
        print("\n")

def drop(mal, regex):
    """Drop a anime based a regex expression"""
    items = remove_completed(mal.find(regex))
    item = select_item(items)
    entry = dict(status=mal.status_codes['dropped'])
    old_status = mal.status_names[item['status']]
    template = {
        'title': color.colorize(item['title'], 'yellow', 'bold'),
        'old-status': color.colorize(old_status, 'green', 'bold'),
        'action': color.colorize('Dropping', 'red', 'bold')

    }

    print(('{action} anime {title} from list '
           '{old-status}'.format_map(template)))
    response = mal.update(item['id'], entry)
    report_if_fails(response)


def add(mal, regex, status="plan to watch"):
    """Add an entry to the user list."""
    results = mal.search(regex)
    selected = select_item(results)

    print("Adding {title} to list as '{status}'".format(
        title=color.colorize(selected["title"], "yellow", "bold"),
        status=status)
    )
    mal.update(
        selected["id"],
        {"status": mal.status_codes[status]},
        action="add"
    )


def stats(mal, username=None):
    """Print user anime stats."""
    # get all the info
    animes = mal.list(stats=True, user=username)
    if not animes:
        print_error("Empty query", "username not found",
                    "could not fetch list for user '{}'".format(username),
                    kill=True)
    user_info = animes.pop("stats")  # remove stats from anime list

    # gather all the numbers
    total_entries = len(animes)
    rewatched, episodes, mean_score, scored = 0, 0, 0, 0
    for anime in animes.values():
        episodes += anime["episode"]  # this is watched episodes
        if anime["rewatching"] != 0:
            rewatched += anime["rewatching"]
            # take into account episodes seen in previous watchings
            episodes += anime["rewatching"] * anime["total_episodes"]

        if anime["score"] != 0:
            scored += 1
        mean_score += anime["score"]

    if scored != 0:
        mean_score /= scored
    # added two for circle colored + space on each list
    line_size = 44 + 2
    # ↑ code for calculating this was so messy I hardcoded instead
    # it's 20 spaces for each of the 'sides' and 4 spaces in between them

    # colored bar. borrowed the bar char from neofetch
    bar = "█"
    colors = ["green", "blue", "yellow", "red", "gray"]
    lists = ["watching", "completed", "onhold", "dropped", "plantowatch"]
    colored = str()
    if total_entries != 0:  # to prevent division by zero
        for i, status in enumerate(lists):
            entries = int(user_info[status])
            bars = round(line_size * (entries / total_entries))
            colored += color.colorize(bar * bars, colors[i])
    else:
        colored = color.colorize(bar * line_size, "white")

    # format the lines to print more easily afterwards
    template = {
        "days": user_info["days_spent_watching"],
        "mean_score": "{:.2f}".format(mean_score),
        "watching": user_info["watching"],
        "completed": user_info["completed"],
        "hold": user_info["onhold"],
        "plan": user_info["plantowatch"],
        "dropped": user_info["dropped"],
        "total_entries": str(total_entries),
        "episodes": str(episodes),
        "rewatched": str(rewatched),
        "padd": "{p}"  # needed to format with padding afterwards
    }

    def point_color(color_name):
        return color.colorize("● ", color_name, "bold")

    lines = [
        "Days: {days}{padd}Mean Score: {mean_score}",
        colored,
        (point_color("green"),
            ["Watching:{padd}{watching}", "Total Entries:{padd}{total_entries}"]),
        (point_color("blue"),
            ["Completed:{padd}{completed}", "Rewatched:{padd}{rewatched}"]),
        (point_color("yellow"),
            ["On-Hold:{padd}{hold}", "Episodes:{padd}{episodes}"]),
        (point_color("red"), ["Dropped:{padd}{dropped}"]),
        (point_color("gray"), ["Plan to Watch:{padd}{plan}"])
    ]
    # add info to lines and format them to look nice
    def padd_str(string, final_size):
        return string.replace("{p}", " " * (final_size - len(string) + len("{p}")))

    lines = [
        padd_str(line.format_map(template), line_size) if not isinstance(line, tuple) else
        # first format each side, then add padding then join with the tab
        line[0] + (" " * 4).join(padd_str(side.format_map(template), 20) for side in line[1])
        for line in lines
    ]

    print(color.colorize("Anime Stats", "white", "underline"))
    print("\n".join(lines))


def find(mal, regex, filtering='all', extra=False, user=None):
    """Find all anime in a certain status given a regex."""
    items = mal.find(regex, extra=extra, user=user)
    if len(items) == 0:
        print(color.colorize("No matches in list ᕙ(⇀‸↼‶)ᕗ", 'red'))
        return

    # filter the results if necessary
    if filtering != 'all':
        items = [x for x in items if x['status_name'] == filtering]

    n_items = color.colorize(str(len(items)), 'cyan', 'underline')
    print("Matched {} items:".format(n_items))

    # pretty print all the animes found
    sorted_items = sorted(items, key=itemgetter('status'), reverse=True)
    for index, item in enumerate(sorted_items):
        anime_pprint(index + 1, item, extra=extra)


def edit(mal, regex, changes):
    """Select and change entry. Opens file with data to change if no
    field was given."""
    # find the correct entry to modify (handles animes not found)
    entry = select_item(mal.find(regex, extra=True))

    if not changes: # open file for user to choose changes manually
        tmp_path = tempfile.gettempdir() + '/mal_tmp'
        editor = os.environ.get('EDITOR', '/usr/bin/vi')
        # write information to tmp file
        with open(tmp_path, 'w') as tmp:
            tmp.write('# change fields for "{}"\n'.format(entry['title']))
            tmp.write('status: {}\n'.format(mal.status_names[entry['status']]))
            for field in ['score', 'tags']:
                tmp.write('{}: {}\n'.format(field, entry[field]))

        # open the file with the default editor
        subprocess.call([editor, tmp_path]) 

        # read back the data into a dict if any changes were made
        with open(tmp_path, 'r') as tmp:
            lines = [l for l in tmp.read().split('\n') if l and not l.startswith('#')]

        # delete tmp file, we don't need it anymore
        os.remove(tmp_path)

        changes = dict()
        for field, value in [tuple(l.split(':')) for l in lines]:
            field, value = field.strip(), value.strip()
            if field == 'status':
                value = str(mal.status_codes[value])
            if str(entry[field]) != value:
                changes[field] = value
        if not changes: return

    # change entry
    for field, new in changes.items():
        if field == 'add_tags':
            if entry.get('tags') is None:
                entry['tags'] = new
            else:
                entry['tags'] += ' ' + new
        else:
            entry[field] = new

    # if the entry didn't have a tag before and none was provived by
    # the user as a change we need to remove the entry from the dict
    # to prevent the api from thinking we want to add the 'None' tag
    if entry.get('tags') is None:
        entry.pop('tags')

    # send it back to update
    response = mal.update(entry['id'], entry)
    report_if_fails(response)


def anime_pprint(index, item, extra=False):
    """Pretty print an anime's information."""
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
    # add formating options for extra info
    if extra:
        template.update({
            'start': item['start_date'] if item['start_date'] != '0000-00-00' else 'NA',
            'finish': item['finish_date'] if item['finish_date'] != '0000-00-00' else 'NA',
            'tags': item['tags']
        })

    message_lines = [
        "{index}: {title}".format_map(template),
        ("{padding}{status} at {remaining} episodes "
         "with score {score} {rewatching}".format_map(template))
    ]

    # the extra information lines
    if extra:
        message_lines.extend([
            "{padding}Started: {start} \t Finished: {finish}".format_map(template),
            "{padding}Tags: {tags}".format_map(template)
        ])

    print('\n'.join(message_lines), "\n")
