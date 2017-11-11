#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vim
import os
import os.path
from leaderf.utils import *
from leaderf.explorer import *
from leaderf.manager import *

from wcwidth import wcswidth
from urllib.request import urlopen
import json

cache_dir = os.path.join(
    os.path.expanduser(os.getenv('XDG_CACHE_HOME', '~/.cache')),
    'github_stars')
cache_dir = os.path.normpath(cache_dir)
cache_file = os.path.join(cache_dir, 'starred_repos')
username = vim.vars['gs#username'].decode()


def parseLine(line):
    line = line.rstrip()
    name, sep, desc = line.partition(" ")
    name = name[:25]
    desc = desc[:50].strip()
    spaces = 30 - wcswidth(name)
    return name + spaces * ' ' + desc


#*****************************************************
# StarsExplorer
#*****************************************************
class StarsExplorer(Explorer):
    def __init__(self):
        self._repo_list = []
        if not os.path.exists(cache_dir):
            os.makedirs(self.cache_dir)

    def getContent(self, *args, **kwargs):
        if not os.path.exists(cache_file):
            return self.getFreshContent()
        elif len(self._repo_list) > 0:
            return self._repo_list
        else:
            self._repo_list = []

            with open(cache_file, 'r') as f:
                for line in f.readlines():
                    self._repo_list.append(parseLine(line))
            return self._repo_list

    def getFreshContent(self, *args, **kwargs):
        lfCmd("echom 'fetching data from GitHub, it may take a while'")
        self._repo_list = []
        with open(cache_file, 'wb') as f:
            page = 0
            while True:
                page += 1
                url = "https://api.github.com/users/%s/starred?per_page=100&page=%d" % (
                    username, page)
                resp = urlopen(url)
                starred_repos = json.load(resp)
                if len(starred_repos) == 0:
                    break
                for repo in starred_repos:
                    line = ("%s %s\n" % (repo['full_name'], ""
                                         if repo['description'] is None else
                                         repo['description']))
                    f.write(line.encode('utf-8'))
                    self._repo_list.append(parseLine(line))
        return self._repo_list

    def getStlCategory(self):
        return "Stars"

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))

    def isFilePath(self):
        return False


#*****************************************************
# StarsExplManager
#*****************************************************
class StarsExplManager(Manager):
    def __init__(self):
        super(StarsExplManager, self).__init__()
        self._match_ids = []

    def _getExplClass(self):
        return StarsExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#Stars#Maps()")

    def _acceptSelection(self, *args, **kwargs):
        if len(args) == 0:
            return
        line = args[0]
        repo = line.split('\t')[0]
        url = "https://github.com/%s" % repo
        lfCmd("call leaderf#Stars#open('%s')" % url)

    def _getDigest(self, line, mode):
        if not line:
            return ''
        return line

    def _getDigestStartPos(self, line, mode):
        return 0

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : open repo in browser')
        help.append('" i : switch to input mode')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append(
            '" ---------------------------------------------------------')
        return help

    def _beforeExit(self):
        super(StarsExplManager, self)._beforeExit()
        for i in self._match_ids:
            lfCmd("silent! call matchdelete(%d)" % i)
        self._match_ids = []

    def removeCache(self):
        if os.path.exists(cache_file):
            os.remove(cache_file)
        lfCmd("echom 'Cache file removed'")


#*****************************************************
# starsExplManager is a singleton
#*****************************************************
starsExplManager = StarsExplManager()

__all__ = ['starsExplManager']
