#coding=utf-8
import urllib2
from urllib2 import HTTPError, URLError
from tParserBase import hrefParser
import os
#for test
import random


class tLogBase(object):
    def __init__(self, baseUrl, basePath, source='online'):
        self.baseUrl = baseUrl
        self.basePath = basePath
        self.source = source
        self.targetPath = os.path.join(basePath, source)
        #
        self.log = None
        #
        self.fileHrefs = []
        self.targets = []
        #
        self.initialize()
        return

    def initialize(self):
        self.logInit()
        return

    def logInit(self):
        self.logPath = os.path.join(self.basePath, '.log')
        if not os.path.isdir(self.logPath):
            os.makedirs(self.logPath)

        if not os.path.exists(os.path.join(self.logPath, '%s.log' % (self.source, ))):
            self.log = {}
        else:
            #todo
            self.log = {}
        return

    def logOutput(self):
        return

    def walk(self, path):
        url = os.path.join(self.baseUrl, path)
        hrefs = self.getHrefs(url)
        if not hrefs:
            return
        dirs, nondirs = [], []
        for oneHref in hrefs:
            if self.isDir(oneHref):
                dirs.append(oneHref)
            else:
                nondirs.append(oneHref)
        for one in dirs:
            targetDir = os.path.join(self.targetPath, path, one)
            if not os.path.isdir(targetDir):
                os.makedirs(targetDir)
        yield path, dirs, nondirs
        for oneDir in dirs:
            newPath = os.path.join(path, oneDir)
            for x in self.walk(newPath):
                yield x
        return

    def getHrefs(self, url):
        req = urllib2.Request(url)
        try:
            resp = urllib2.urlopen(req)
        except (HTTPError, URLError):
            return
        contentType = resp.headers.get('Content-Type', '').lower()
        if contentType.startswith('text/'):
            pageData = resp.read()
            parser = hrefParser()
            parser.feed(pageData)
            return parser.getHrefs()
        return

    def isDir(self, url):
        return url.endswith('/')

    def isTarget(self, url):
        return url.endswith('.gz')

    def isModified(self, key):
        return random.choice([key, False])

    def fileDownload(self, key):
        url = os.path.join(self.baseUrl, key)
        print 'downloading:%s' % (url, )
        req = urllib2.Request(url)
        try:
            resp = urllib2.urlopen(req)
            data = resp.read()
            size = len(data)
            fpath = os.path.join(self.targetPath, key)
            with file(fpath, 'wb') as f:
                f.write(data)
                self.log[key] = size
            return
        except (HTTPError, URLError, IOError):
            return

    def fileSave(self, key):
        return

    def fileOutput(self, key):
        return

    def fileSize(self, key):
        return

    def fileModified(self, key):
        return

    def logOutput(self):
        with file(os.path.join(self.logPath, '%s.log' % (self.source, )), 'w') as log:
            for l in self.log:
                line = '%s %s\n' % (l, self.log[l])
                log.write(line)
        return

    def run(self):
        for path, dirs, files in self.walk('./'):
            for one in files:
                self.fileHrefs.append(os.path.join(path, one))
        #过滤未修改的文件
        self.fileHrefs = filter(self.isModified, self.fileHrefs)

        #要下载的目标文件
        self.targets = filter(self.isTarget, self.fileHrefs)
        for t in self.targets:
            self.fileDownload(t)
        self.logOutput()


baseUrl = 'http://test.com:50001/'
path = '/home/dtynn/work/test/file_server_get'
a = tLogBase(baseUrl, path)
a.run()