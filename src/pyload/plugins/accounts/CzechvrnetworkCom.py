# -*- coding: utf-8 -*-

# import re
# import time
from datetime import timedelta
import json

import pycurl
# from pyload.core.network.http.exceptions import BadHeader

from ..base.account import BaseAccount

__HERESPHERE_BASE_URL__ = "https://beta.czechvrnetwork.com/heresphere"

class CzechvrnetworkCom(BaseAccount):
    __name__ = "CzechvrnetworkCom"
    __type__ = "account"
    __version__ = "0.1"
    __status__ = "testing"

    __description__ = """CzechVR Network account plugin"""
    __license__ = "GPLv3"
    __authors__ = [
        ("paulpaul999", "no-mail@github.com")
    ]

    LOGIN_TIMEOUT = timedelta(days=7).total_seconds()

    def grab_info(self, user, password, data):
        premium = False
        validuntil = None
        trafficleft = None

        token = data.get('token')

        self.req.http.c.setopt(pycurl.USERAGENT, "HereSphere")
        self.req.http.c.setopt(
            pycurl.HTTPHEADER, [f"auth-token: {token}"]
        )
        response_ = self.load(
            __HERESPHERE_BASE_URL__,
            post=True,
            cookies=False,
            decode=False
        )
        response = json.loads(response_)

        premium = response.get('access') == 1

        return {
            "premium": premium,
            "validuntil": validuntil,
            "trafficleft": trafficleft,
        }

    def signin(self, user, password, data):
        self.req.http.c.setopt(pycurl.USERAGENT, "HereSphere")
        post_payload = json.dumps( {"username": user, "password": password} )
        response_ = self.load(
            f"{__HERESPHERE_BASE_URL__}/auth",
            post=post_payload,
            cookies=False,
            decode=False
        )
        response = json.loads(response_)

        if not response['access'] == 1:
            self.fail_login()

        data['token'] = response['auth-token']
