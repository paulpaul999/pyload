# -*- coding: utf-8 -*-

import re
import urllib

from module.plugins.Crypter import Crypter
from module.plugins.internal.SimpleHoster import create_getInfo, getFileURL, set_cookies
from module.utils import html_unescape


class SimpleDereferer(Crypter):
    __name__    = "SimpleDereferer"
    __type__    = "crypter"
    __version__ = "0.12"

    __pattern__ = r'^unmatchable$'
    __config__  = []  #@TODO: Remove in 0.4.10

    __description__ = """Simple dereferer plugin"""
    __license__     = "GPLv3"
    __authors__     = [("Walter Purcaro", "vuolter@gmail.com")]


    """
    Following patterns should be defined by each crypter:

      LINK_PATTERN: Regex to catch the redirect url in group(1)
        example: LINK_PATTERN = r'<div class="link"><a href="(.+?)"'

      OFFLINE_PATTERN: (optional) Checks if the page is unreachable
        example: OFFLINE_PATTERN = r'File (deleted|not found)'

      TEMP_OFFLINE_PATTERN: (optional) Checks if the page is temporarily unreachable
        example: TEMP_OFFLINE_PATTERN = r'Server maintainance'


    You can override the getLinks method if you need a more sophisticated way to extract the redirect url.
    """

    LINK_PATTERN = None

    TEXT_ENCODING = False
    COOKIES       = True


    def decrypt(self, pyfile):
        link = getFileURL(self, pyfile.url)

        if not link:
            try:
                link = urllib.unquote(re.match(self.__pattern__, pyfile.url).group('LINK'))

            except Exception:
                self.prepare()
                self.preload()
                self.checkStatus()

                link = self.getLink()

        if link.strip():
            self.urls = [link.strip()]  #@TODO: Remove `.strip()` in 0.4.10

        elif not self.urls and not self.packages:  #@TODO: Remove in 0.4.10
            self.fail(_("No link grabbed"))


    def prepare(self):
        self.info = {}
        self.html = ""

        self.req.setOption("timeout", 120)

        if isinstance(self.COOKIES, list):
            set_cookies(self.req.cj, self.COOKIES)


    def preload(self):
        self.html = self.load(self.pyfile.url, cookies=bool(self.COOKIES), decode=not self.TEXT_ENCODING)

        if isinstance(self.TEXT_ENCODING, basestring):
            self.html = unicode(self.html, self.TEXT_ENCODING)


    def checkStatus(self):
        if hasattr(self, "OFFLINE_PATTERN") and re.search(self.OFFLINE_PATTERN, self.html):
            self.offline()

        elif hasattr(self, "TEMP_OFFLINE_PATTERN") and re.search(self.TEMP_OFFLINE_PATTERN, self.html):
            self.tempOffline()


    def getLink(self):
        try:
            return html_unescape(re.search(self.LINK_PATTERN, self.html).group(1).decode('unicode-escape'))  #@TODO: Move this check to plugin `load` method in 0.4.10

        except Exception:
            pass
