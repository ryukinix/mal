#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

# stdlib
import re
from xml.etree import cElementTree as ET
from datetime import datetime

# 3rd party
import requests
from decorating import animated

# self-package
from mal.utils import checked_connection, checked_regex, checked_cancer
from mal import setup


class MyAnimeList(object):
    """Does all the actual communicating with the MAL api."""
    base_url = 'https://myanimelist.net/api'
    user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/34.0.1847.116 Safari/537.36')

    status_names = {
        1: 'watching',
        2: 'completed',
        3: 'on hold',
        4: 'dropped',
        6: 'plan to watch',  # not a typo
        7: 'rewatching'  # this not exists in API
    }                    # check list function about 'rewatching'

    # reverse of status_names dict
    status_codes = {v: k for k, v in status_names.items()}

    def __init__(self, username, password, date_format=setup.DEFAULT_DATE_FORMAT):
        self.username = username
        self.password = password
        self.date_format = date_format

    @checked_connection
    @animated('validating login')
    def validate_login(self):
        r = requests.get(
            self.base_url + '/account/verify_credentials.xml',
            auth=(self.username, self.password),
            headers={'User-Agent': self.user_agent}
        )

        return r.status_code

    @classmethod
    def login(cls, config):
        """Create an instante of MyAnimeList and log it in."""
        username = config[setup.LOGIN_SECTION]['username']
        password = config[setup.LOGIN_SECTION]['password']
        date_format = config[setup.CONFIG_SECTION]['date_format']

        mal = cls(username, password, date_format)

        # 401 = unauthorized
        if mal.validate_login() == 401:
            return None

        return mal

    @checked_cancer
    @checked_connection
    @animated('searching in database')
    def search(self, query):
        payload = dict(q=query)

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

    @checked_cancer
    @checked_connection
    @animated('preparing animes')
    def list(self, status='all', type='anime', extra=False, stats=False, user=None):
        username = self.username if not user else user

        payload = dict(u=username, status=status, type=type)
        r = requests.get(
            'https://myanimelist.net/malappinfo.php',
            params=payload,
            headers={'User-Agent': self.user_agent}
        )
        if "_Incapsula_Resource" in r.text:
            raise RuntimeError("Request blocked by Incapsula protection")

        result = dict()
        for raw_entry in ET.fromstring(r.text):
            entry = dict((attr.tag, attr.text) for attr in raw_entry)

            # anime information
            if 'series_animedb_id' in entry:
                entry_id = int(entry['series_animedb_id'])
                result[entry_id] = {
                    'id': entry_id,
                    'title': entry['series_title'],
                    'episode': int(entry['my_watched_episodes']),
                    'status': int(entry['my_status']),
                    'score': int(entry['my_score']),
                    'total_episodes': int(entry['series_episodes']),
                    'rewatching': int(entry['my_rewatching'] or 0),
                    'status_name': self.status_names[int(entry['my_status'])],
                }
                # if was rewatching, so the status_name is rewatching
                if result[entry_id]['rewatching']:
                    result[entry_id]['status_name'] = 'rewatching'

                # add extra info about anime if needed
                if extra:
                    extra_info = {
                        'start_date': self._fdate(entry['my_start_date']),
                        'finish_date': self._fdate(entry['my_finish_date']),
                        'tags': entry['my_tags']
                    }
                    result[entry_id].update(extra_info)

            # user stats
            if stats and 'user_id' in entry:
                result['stats'] = {}
                # copy entry dict to result['stats'] without all the 'user_'
                for k, v in entry.items():
                    result['stats'][k.replace('user_', '')] = v

        return result

    def _fdate(self, date, api_format='%Y-%m-%d'):
        """Format date based on the user config format"""
        if any(int(s) == 0 for s in date.split('-')):
            return date
        return datetime.strptime(date, api_format).strftime(self.date_format)

    @checked_regex
    @animated('matching animes')
    def find(self, regex, status='all', extra=False, user=None):
        result = []
        for value in self.list(status, extra=extra, user=user).values():
            if re.search(regex, value['title'], re.I):
                result.append(value)
        return result

    @checked_cancer
    @checked_connection
    @animated('updating')
    def update(self, item_id, entry, action="update"):
        tree = ET.Element('entry')
        for key, val in entry.items():
            ET.SubElement(tree, key).text = str(val)

        encoded = ET.tostring(tree).decode('utf-8')
        xml_item = '<?xml version="1.0" encoding="UTF-8"?>' + encoded

        payload = {'data': xml_item}
        r = requests.post(
            self.base_url + '/animelist/{}/'.format(action) + str(item_id) + '.xml',
            data=payload,
            auth=(self.username, self.password),
            headers={'User-Agent': self.user_agent}
        )
        return r.status_code
