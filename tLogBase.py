#coding=utf-8
import urllib2
from urllib2 import HTTPError
from tParserBase import hrefParser
import os


class tLogBase(object):
    targetExt = []

    def __init__(self):
        self.initialize()
        return

    def initialize(self):
        return

    def getHrefs(self, url):
        req = urllib2.Request(url)
        try:
            resp = urllib2.urlopen(req)
        except HTTPError:
            return
        contentType = resp.headers.get('Content-type', '').lower()
        if contentType and contentType.startswith('text/'):
            pageData = resp.read()
            parser = hrefParser()
            parser.feed(pageData)
            return parser.getHrefs()
        return

    def walk(self, url):
        hrefs = self.getHrefs(url)
        if not hrefs:
            return
        dirs = filter(lambda x: self.isdir(x), hrefs)
        nondirs = filter(lambda x: not self.isdir(x), hrefs)
        print '!!!!!', dirs
        yield url, dirs, nondirs
        for dir in dirs:
            new_url = os.path.join(url, dir)
            for x in self.walk(new_url):
                yield x

    def isdir(self, href):
        return href.endswith('/')


baseUrl = 'http://test.com:50001'
a = tLogBase()
aw = a.walk(baseUrl)
for one in aw:
    print one