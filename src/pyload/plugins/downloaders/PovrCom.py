# -*- coding: utf-8 -*-
# Inspired by CloudzillaTo Plugin

import json
import pycurl

# from pyload.core.utils import parse
from ..base.simple_downloader import SimpleDownloader


def select_max_resolution_(sources):
    for medium in sorted(sources, key=lambda m: m.get('resolution'), reverse=True):
        return medium

def to_url_style_str_(string):
    return string.lower().replace(' ','-')

def get_studio_name_(tags):
    prefix_ = 'Studio:'
    for tag in tags:
        tag_name = tag.get('name','')
        if tag_name.startswith(prefix_):
            studio_name = tag_name[len(prefix_):]
            return studio_name


class PovrCom(SimpleDownloader):
    __name__ = "PovrCom"
    __type__ = "downloader"
    __version__ = "0.1"
    __status__ = "testing"

    __pattern__ = r"https?://(?:www\.)?povr\.com/vr-porn/(?P<ID>[^/\s]+)"
    __config__ = [
        ("enabled", "bool", "Activated", True),
        ("use_premium", "bool", "Use premium account if available", True),
        ("fallback", "bool", "Fallback to free download if premium fails", True),
        ("chk_filesize", "bool", "Check file size", True),
        ("max_wait", "int", "Reconnect if waiting time is greater than minutes", 10),
    ]

    __description__ = """POVR.com downloader plugin"""
    __license__ = "GPLv3"
    __authors__ = [("paulpaul999", "no-mail@github.com")]

    COOKIES = False

    DIRECT_LINK = False

    LOGIN_ACCOUNT = True
    LOGIN_PREMIUM = True

    TEXT_ENCODING = False

    def setup(self):
        super(PovrCom, self).setup()

        self.data = "workaround-to-prevent-preload-routine"

        token = self.account.info['data']['token']
        
        # self.req.http.c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_1_0)
        self.req.http.c.setopt(pycurl.USERAGENT, "HereSphere")
        self.req.http.c.setopt(
            pycurl.HTTPHEADER, [f"auth-token: {token}"]
        )

    def handle_premium(self, pyfile):
        url_id = self.info['pattern']['ID']
        url_scene_name, scene_id = url_id.rsplit('-',1)

        pyfile.name = url_id

        response_ = self.load(
            f"https://povr.com/heresphere/{scene_id}",
            post=True,
            cookies=False,
            decode=False
        )
        response = json.loads(response_)

        filename_prefix = to_url_style_str_(get_studio_name_(response['tags']))
        filename = f"{filename_prefix}-{url_scene_name}-180_180x180_3dh_LR.mp4"

        # TODO: Support scenes from non-7k era
        medium_source = None
        for medium in response['media']:
            if medium['name'] == 'h265':
                medium_source = select_max_resolution_(medium['sources'])
                break

        if medium_source == None:
            self.fail("Could not select a suitable format/resolution variant.")

        self.link = medium_source['url']
        pyfile.name = filename
