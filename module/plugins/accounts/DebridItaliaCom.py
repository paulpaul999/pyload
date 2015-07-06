# -*- coding: utf-8 -*-

import re
import time

from module.plugins.internal.Account import Account


class DebridItaliaCom(Account):
    __name__    = "DebridItaliaCom"
    __type__    = "account"
    __version__ = "0.15"

    __description__ = """Debriditalia.com account plugin"""
    __license__     = "GPLv3"
    __authors__     = [("stickell", "l.stickell@yahoo.it"),
                       ("Walter Purcaro", "vuolter@gmail.com")]


    WALID_UNTIL_PATTERN = r'Premium valid till: (.+?) \|'


    def load_account_info(self, user, req):
        info = {"premium": False, "validuntil": None, "trafficleft": None}
        html = self.load("http://debriditalia.com/", req=req)

        if 'Account premium not activated' not in html:
            m = re.search(self.WALID_UNTIL_PATTERN, html)
            if m:
                validuntil = time.mktime(time.strptime(m.group(1), "%d/%m/%Y %H:%M"))
                info = {"premium": True, "validuntil": validuntil, "trafficleft": -1}
            else:
                self.log_error(_("Unable to retrieve account information"))

        return info


    def login(self, user, data, req):
        html = self.load("https://debriditalia.com/login.php",
                        get={'u': user, 'p': data['password']}, req=req)

        if 'NO' in html:
            self.wrong_password()
