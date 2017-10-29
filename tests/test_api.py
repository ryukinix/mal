
import unittest
from unittest import mock
from unittest.mock import ANY

import requests

from pprint import pprint

from mal import api
from mal import setup
from tests.mal_responses import MalListResponseBuilder
from tests.mal_responses import MalSearchResponseBuilder

DATE_FORMAT = '%d-%m-%Y'
MOCK_USER = 'dummy_user'
MOCK_PASS = 'dummy_pass'
MOCK_CONFIG = {
    setup.LOGIN_SECTION: {
        'username': MOCK_USER,
        'password': MOCK_PASS
    },
    setup.CONFIG_SECTION: {
        'date_format': DATE_FORMAT
    }
}


class TestApiList(unittest.TestCase):

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

    @mock.patch.object(requests, 'get')
    def test_list_anime_single_extended(self, mock_response_get):
        list = MalListResponseBuilder()
        list.set_profile({'user_name': 'any'})
        list.add_series({
            'series_animedb_id': 2,
            'series_title': 'anime2',
            'my_start_date': '2016-01-01',
            'my_finish_date': '2016-01-01',
            'my_tags': 'moe'
        })
      
        mock_response_get.return_value = mock.Mock(
            text=list.get_response_xml())
        result = self.mal.list(extra=True)

        self.assertTrue(2 in result)
        anime = result[2]

        anime_props_valid = lambda x: all(
            anime.get(k) == v for k, v in x.items())

        self.assertTrue(DATE_FORMAT == '%d-%m-%Y')
        self.assertTrue(anime_props_valid({
            'title': 'anime2',
            'start_date': '01-01-2016',
            'finish_date': '01-01-2016',
            'tags': 'moe'
        }))

    @mock.patch.object(requests, 'get')
    def test_list_anime_single_with_stats(self, mock_response_get):
        list = MalListResponseBuilder()
        list.set_profile({
            'user_id': 1,
            'user_name': 'name1',
            'user_completed': 2,
            'user_onhold': 3,
            'user_dropped': 4,
            'user_days_spent_watching': 5.0,
            'user_watching': 6,
            'user_plantowatch': 7
        })
        list.add_series({
            'series_animedb_id': 3,
            'series_title': 'anime3',
        })
      
        mock_response_get.return_value = mock.Mock(
            text=list.get_response_xml())
        result = self.mal.list(stats=True)

        self.assertTrue(3 in result)
        anime = result[3]
        
        self.assertTrue('stats' in result)
        anime_stats_props_valid = lambda x: all(
            result['stats'].get(k) == v for k, v in x.items())

        self.assertTrue(anime.get('title') == 'anime3')
        self.assertTrue(anime_stats_props_valid({
            'id': '1',
            'name': 'name1',
            'completed': '2',
            'onhold': '3',
            'dropped': '4',
            'days_spent_watching': '5.0',
            'watching': '6',
            'plantowatch': '7'
        }))


class TestApiFind(unittest.TestCase):

    @mock.patch.object(api.MyAnimeList, 'validate_login')
    def setUp(self, mock_validate_login):
        mock_validate_login.return_value = 200
        self.mal = api.MyAnimeList.login(MOCK_CONFIG)

    @mock.patch.object(requests, 'get')
    def test_find_anime_found_and_lost(self, mock_response_get):
        list = MalListResponseBuilder()
        list.set_profile({'user_name': 'any'})
        list.add_series({
            'series_animedb_id': 1,
            'series_title': 'found_anime'
        })
        list.add_series({
            'series_animedb_id': 2,
            'series_title': 'lost_anime'
        })
       
        mock_response_get.return_value = mock.Mock(
            text=list.get_response_xml())
        results = self.mal.find('found_anime')

        self.assertTrue(len(results) == 1)
        anime = results[0]
        self.assertTrue(anime.get('title') == 'found_anime')

    @mock.patch.object(requests, 'get')
    def test_find_anime_found_more_than_one(self, mock_response_get):
        list = MalListResponseBuilder()
        list.set_profile({'user_name': 'any'})
        list.add_series({
            'series_animedb_id': 1,
            'series_title': 'found_anime'
        })
        list.add_series({
            'series_animedb_id': 2,
            'series_title': 'found_anime2'
        })
       
        mock_response_get.return_value = mock.Mock(
            text=list.get_response_xml())
        results = self.mal.find('found_anime')

        self.assertTrue(len(results) == 2)
        first_title = results[0].get('title')
        second_title = results[1].get('title')

        self.assertTrue(
            first_title == 'found_anime' or second_title == 'found_anime')
        self.assertTrue(
            first_title == 'found_anime2' or second_title == 'found_anime2')


class TestApiLogin(unittest.TestCase):

    @mock.patch.object(api.MyAnimeList, 'validate_login')
    def test_login_authorized(self, mock_validate_login):
        mock_validate_login.return_value = 200
        result = api.MyAnimeList.login(MOCK_CONFIG)
        self.assertTrue(isinstance(result, api.MyAnimeList))

    @mock.patch.object(api.MyAnimeList, 'validate_login')
    def test_login_unauthorized(self, mock_validate_login):
        mock_validate_login.return_value = 401
        result = api.MyAnimeList.login(MOCK_CONFIG)
        self.assertTrue(result == None)


class TestApiValidateLogin(unittest.TestCase):

    @mock.patch.object(requests, 'get')
    def test_validate_login(self, mock_response_get):
        mal = api.MyAnimeList(MOCK_CONFIG)
        mock_status_code = 1
        mock_response_get.return_value = mock.Mock(
            status_code=mock_status_code)
        result = mal.validate_login()

        mock_response_get.assert_called_with(
            'https://myanimelist.net/api/account/verify_credentials.xml',
            auth=(MOCK_USER, MOCK_PASS),
            headers=ANY
        )

        self.assertTrue(result == mock_status_code)


class TestApiSearch(unittest.TestCase):

    @mock.patch.object(api.MyAnimeList, 'validate_login')
    def setUp(self, mock_validate_login):
        mock_validate_login.return_value = 200
        self.mal = api.MyAnimeList.login(MOCK_CONFIG)

    @mock.patch.object(requests, 'get')
    def test_search_found(self, mock_response_get):
        search_query = 'test'
        search_results = MalSearchResponseBuilder()
        search_results.add_result({'title': search_query})
        mock_response_get.return_value = mock.Mock(
            status_code=200,
            text=search_results.get_response_xml()
        )
        results = self.mal.search(search_query)

        mock_response_get.assert_called_with(
            ANY,
            params=dict(q=search_query),
            auth=ANY,
            headers=ANY
        )

        self.assertTrue(len(results) == 1)
        first_result = results[0]
        self.assertTrue(first_result['title'] == search_query)

    @mock.patch.object(requests, 'get')
    def test_search_found_more_than_one(self, mock_response_get):
        search_query = 'test'
        search_results = MalSearchResponseBuilder()
        search_results.add_result({'title': 'test1'})
        search_results.add_result({'title': 'test2'})
        mock_response_get.return_value = mock.Mock(
            status_code=200,
            text=search_results.get_response_xml()
        )
        results = self.mal.search(search_query)

        mock_response_get.assert_called_with(
            ANY,
            params=dict(q=search_query),
            auth=ANY,
            headers=ANY
        )

        self.assertTrue(len(results) > 1)
        for result in results:
            self.assertTrue(search_query in result['title'])

    @mock.patch.object(requests, 'get')
    def test_search_not_found(self, mock_response_get):
        search_query = 'not found'
        mock_response_get.return_value = mock.Mock(
            status_code=204
        )
        results = self.mal.search(search_query)

        mock_response_get.assert_called_with(
            ANY,
            params=dict(q=search_query),
            auth=ANY,
            headers=ANY
        )

        self.assertTrue(len(results) == 0)


if __name__ == '__main__':
    unittest.main()
