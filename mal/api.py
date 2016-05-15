#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyleft © Manoel Vilela
#
#

import re
import requests
from xml.etree import cElementTree as ET


class MyAnimeList(object):
    base_url = 'http://myanimelist.net/api'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'

    status_names = {
        1: 'watching',
        2: 'completed',
        3: 'on hold',
        4: 'dropped',
        6: 'plan to watch',  # not a typo
        7: 'rewatching' # we have rewatching here too, label for completed
    }

    status_codes = {v: k for k, v in status_names.items()}

    def __init__(self, config):
        self.username = config['username']
        self.password = config['password']

    def get_status_name(self, status_code):
        return self.status_names[status_code]

    def search(self, query):
        payload = {'q': query}

        r = requests.get(
            self.base_url + '/anime/search.xml',
            params=payload,
            auth=(self.username, self.password),
            headers={'User-Agent': self.user_agent}
        )

        if (r.status_code == 204):
            return []

        elements = ET.fromstring(r.text)
        return [dict((attr.tag, attr.text) for attr in el) for el in elements]

    def list(self, status='all', username=None):
        if username is None:
            username = self.username

        payload = {'u': username, 'status': status, 'type': 'anime'}
        r = requests.get(
            'http://myanimelist.net/malappinfo.php',
            params=payload,
            headers={'User-Agent': self.user_agent}
        )

        if "_Incapsula_Resource" in r.text:
            raise RuntimeError("Request blocked by Incapsula protection")

        result = dict()
        for raw_entry in ET.fromstring(r.text):
            entry = dict((attr.tag, attr.text) for attr in raw_entry)

            if 'series_animedb_id' in entry:
                entry_id = int(entry['series_animedb_id'])
                result[entry_id] = {
                    'id': entry_id,
                    'title': entry['series_title'],
                    'episode': int(entry['my_watched_episodes']),
                    'status': int(entry['my_status']),
                    'score': int(entry['my_score']),
                    'total_episodes': int(entry['series_episodes']),
                    'rewatching': int(entry['my_rewatching']) if entry['my_rewatching'] else 0,
                    'status_name': self.get_status_name(int(entry['my_status'])),
                }
                # if was rewatching, so the status_name is rewatching
                if result[entry_id]['rewatching']:
                    result[entry_id]['status_name'] = 'rewatching'

        return result

    def find(self, regex, status='all', username=None):
        result = []
        for key, val in self.list(status, username).items():
            if re.search(regex, val['title'], re.I):
                result.append(val)
        return result

    def update(self, item_id, entry):
        tree = ET.Element('entry')
        for key, val in entry.items():
            ET.SubElement(tree, key).text = str(val)

        encoded = ET.tostring(tree).decode('utf-8')
        xml_item = '<?xml version="1.0" encoding="UTF-8"?>' + encoded

        payload = {'data': xml_item}
        r = requests.post(
            self.base_url + '/animelist/update/' + str(item_id) + '.xml',
            data=payload,
            auth=(self.username, self.password),
            headers={'User-Agent': self.user_agent}
        )
        return r.status_code
