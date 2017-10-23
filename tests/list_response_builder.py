
PROFILE = {
    'shared': {
        'user_id': 0,
        'user_name': '',
        'user_completed': 0,
        'user_onhold': 0,
        'user_dropped': 0,
        'user_days_spent_watching': 0.0
    },
    'anime': {
        'user_watching': 0,
        'user_plantowatch': 0
    },
    'manga': {
        'user_reading': 0,
        'user_plantoread': 0
    }
}


SERIES = {
    'shared': {
        'series_title': '',
        'series_synonyms': '',
        'series_type': 0,
        'series_status': 0,
        'series_start': '0000-00-00',
        'series_end': '0000-00-00',
        'series_image': '',
        'my_id': 0,
        'my_start_date': '0000-00-00',
        'my_finish_date': '0000-00-00',
        'my_score': 0,
        'my_status': 0,
        'my_last_updated': 0,
        'my_tags': ''
    },
    'anime': {
        'series_animedb_id': 0,
        'series_episodes': 0,
        'my_watched_episodes': 0,
        'my_rewatching': 0,
        'my_rewatching_ep': 0,
    },
    'manga': {
        'series_mangadb_id': 0,
        'series_chapters': 0,
        'series_volumes': 0,
        'my_read_chapters': 0,
        'my_read_volumes': 0,
        'my_rereadingg': 0,
        'my_rereading_chap': 0,
    }
}


class MalListResponseBuilder(object):

    def __init__(self, type='anime'):
        self.type = type
        self.myinfo = ''
        self.series = ''

    def set_profile(self, profile_options):
        all_options = PROFILE['shared'].copy()
        all_options.update(PROFILE[self.type])
        all_options.update(profile_options)
        
        result = ''
        for key, value in all_options.items():
            result += '<{0}>{1}</{0}>'.format(key, value)

        self.myinfo = '<myinfo>{0}</myinfo>'.format(result)

    def add_series(self, series_options):
        all_options = SERIES['shared'].copy()
        all_options.update(SERIES[self.type])
        all_options.update(series_options)

        result = ''
        for key, value in all_options.items():
            result += '<{0}>{1}</{0}>'.format(key, value)

        self.series += '<{0}>{1}</{0}>'.format(self.type, result)

    def get_response_xml(self):
        xml_head = '<?xml version="1.0" encoding="UTF-8"?>'
        return '<myanimelist>{0}{1}</myanimelist>'.format(
            self.myinfo, self.series)
