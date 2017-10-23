
import unittest
from unittest import mock

import requests

from mal import api
from mal import setup
from tests.list_response_builder import MalListResponseBuilder


MOCK_CONFIG = {
    setup.LOGIN_SECTION: {
        'username': 'dummy_user',
        'password': 'dummy_pass'
    },
    setup.CONFIG_SECTION: {
        'date_format': '%Y-%m-%d'
    }
}


class TestApi(unittest.TestCase):

    @mock.patch.object(api.MyAnimeList, 'validate_login')
    def setUp(self, mock_validate_login):
        mock_validate_login.return_value = 200
        self.mal = api.MyAnimeList.login(MOCK_CONFIG)

    @mock.patch.object(requests, 'get')
    def test_list_anime_single(self, mock_response_get):

        list = MalListResponseBuilder()
        list.set_profile({'user_name': 'any'})
        list.add_series({
            'series_animedb_id': 1,
            'series_title': 'anime1',
            'my_watched_episodes': 5,
            'my_status': 4,
            'my_score': 3,
            'series_episodes': 2,
            'my_rewatching': 1})

        text = list.get_response_xml()       
        mock_response_get.return_value = mock.Mock(
            text=list.get_response_xml())
        result = self.mal.list()

        self.assertTrue(1 in result)
        anime = result[1]

        anime_props_valid = lambda x: all(
            anime.get(k) == v for k, v in x.items())

        self.assertTrue(anime_props_valid({
            'title': 'anime1',
            'id': 1,
            'episode': 5,
            'status': 4,
            'score': 3,
            'total_episodes': 2,
            'rewatching': 1,
            'status_name': 'rewatching'
        }))


if __name__ == '__main__':
    unittest.main()
