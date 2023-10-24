# -*- coding: utf-8 -*-
# Inspired by CloudzillaTo Plugin

import json
import pycurl

from pyload.core.utils import parse
from ..base.simple_downloader import SimpleDownloader


class BadoinkVR(SimpleDownloader):
    __name__ = "BadoinkVR"
    __type__ = "downloader"
    __version__ = "0.1"
    __status__ = "testing"

    __pattern__ = r"https://(?:www\.)?(?P<P>badoinkvr|kinkvr|babevr|vrcosplayx)\.com/(members/)?[^/]+/(?P<ID>[^/\s]+)"
    __config__ = [
        ("enabled", "bool", "Activated", True),
        ("use_premium", "bool", "Use premium account if available", True),
        ("fallback", "bool", "Fallback to free download if premium fails", True),
        ("chk_filesize", "bool", "Check file size", True),
        ("max_wait", "int", "Reconnect if waiting time is greater than minutes", 10),
    ]

    __description__ = """BadoinkVR.com downloader plugin"""
    __license__ = "GPLv3"
    __authors__ = [("paulpaul999", "no-mail@github.com")]

    COOKIES = False

    DIRECT_LINK = False

    LOGIN_ACCOUNT = True
    LOGIN_PREMIUM = True

    TEXT_ENCODING = False

    def setup(self):
        super(BadoinkVR, self).setup()

        self.data = "workaround-to-prevent-preload-routine"

        token = self.account.info['data']['token']
        
        self.req.http.c.setopt(pycurl.USERAGENT, "HereSphere")
        self.req.http.c.setopt(
            pycurl.HTTPHEADER, [f"auth-token: {token}"]
        )

    def handle_premium(self, pyfile):
        site_domain = self.info['pattern']['P']
        url_id = self.info['pattern']['ID']
        scene_id = url_id.rsplit('-',1)[-1]

        pyfile.name = url_id

        response_ = self.load(
            f"https://{site_domain}.com/heresphere/video/{scene_id}",
            post=True,
            cookies=False,
            decode=False
        )
        response = json.loads(response_)

        for medium in response['media']:
            if medium['name'] == '7k':
                self.link = medium['sources'][0]['url']
                break

        pyfile.name = parse.name(self.link)
