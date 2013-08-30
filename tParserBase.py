#coding=utf-8
from HTMLParser import HTMLParser


class hrefParser(HTMLParser):
    hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = filter(lambda x: x[0] == 'href', attrs)
            if href:
                self.hrefs.append(href[0][1])

    def getHrefs(self):
        return self.hrefs