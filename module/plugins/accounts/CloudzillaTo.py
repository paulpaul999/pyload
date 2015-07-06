# -*- coding: utf-8 -*-

import re

from module.plugins.internal.Account import Account


class CloudzillaTo(Account):
    __name__    = "CloudzillaTo"
    __type__    = "account"
    __version__ = "0.04"

    __description__ = """Cloudzilla.to account plugin"""
    __license__     = "GPLv3"
    __authors__     = [("Walter Purcaro", "vuolter@gmail.com")]


    PREMIUM_PATTERN = r'<h2>account type</h2>\s*Premium Account'


    def load_account_info(self, user, req):
        html = self.load("http://www.cloudzilla.to/", req=req)

        premium = True if re.search(self.PREMIUM_PATTERN, html) else False

        return {'validuntil': -1, 'trafficleft': -1, 'premium': premium}


    def login(self, user, data, req):
        html = self.load("https://www.cloudzilla.to/",
                        post={'lusername': user,
                              'lpassword': data['password'],
                              'w'        : "dologin"}, req=req)

        if "ERROR" in html:
            self.wrong_password()
