# coding: utf-8
from __future__ import unicode_literals

import re
from urllib.parse import urlparse

from .common import InfoExtractor
from .. import utils


class ShuiGuoPaiIE(InfoExtractor):
    IE_NAME = 'ShuiGuoPai'
    _VALID_URL = r'''(?x)
                         (?:https?://)?(?:www\.)?
                             shuiguopai\.com/play-details/1/(?P<id>\d+)'''
    _TEST = {
        'url': 'https://shuiguopai.com/play-details/1/556',
        'md5': 'bbbab114e2915107ffb2e78ccd185447',
        'info_dict': {
            'id': '556',
            'ext': 'mp4',
            'title': '黑丝岳母真风骚，累坏女婿大肉屌！',
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        alternate_host_page = self._download_webpage('https://sgp2.fun/settings/sgp2.fun.ios.js', video_id)
        alternate_host = self._search_regex(
            r'''("|')watchNow("|')\s*:\s*("|')(?P<alturl>(.*?))("|')''',
            alternate_host_page, 'ALTURL', group="alturl"
        )
        alt_url = urlparse(url)._replace(netloc=urlparse(alternate_host).netloc).geturl()
        try:
            webpage = self._download_webpage(url, video_id, timeout=2)
        except utils.ExtractorError:
            webpage = self._download_webpage(alt_url, video_id, timeout=2)
        title = self._html_search_regex(r'(?s)<title\b[^>]*>(.*)</title>', webpage, 'title',
                                        default=None) or self._og_search_title(webpage)
        url = self._search_regex(
            r'''(?<!encryption_)url:("|')(?P<url>(.*?m3u8))("|')''',
            webpage, 'URL', group="url").replace('\\u002F', '/')
        test_url = utils.url_or_none(url)
        if not test_url:
            raise utils.ExtractorError('Invalid audio URL %s' % (url,))
        return {
            'id': video_id,
            'title': title,
            'ext': 'mp4',
            'url': test_url,
        }
