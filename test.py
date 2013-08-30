#coding=utf-8
import urllib2
from HTMLParser import HTMLParser

url = 'http://test.com:50001'
url = 'http://t-test-public.qiniudn.com/viewthread_fastpost_w.png'

req = urllib2.Request(url)

resp = urllib2.urlopen(req)
contentType = resp.headers.get('Content-type', '').lower()
data = resp.read()

#print data


class hrefParser(HTMLParser):
    hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = filter(lambda x: x[0] == 'href', attrs)
            if href:
                self.hrefs.append(href[0][1])

    def hrefOutput(self):
        return self.hrefs


if contentType.startswith('text/'):
    parser = hrefParser()

    parser.feed(data)
    print parser.hrefOutput()
else:
    print 'Not Html'