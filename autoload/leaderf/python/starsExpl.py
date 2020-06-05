#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import os.path
from urllib.request import Request, urlopen

from wcwidth import wcswidth

import vim
from leaderf.explorer import *
from leaderf.manager import *
from leaderf.utils import *

cache_dir = os.path.join(
    os.path.expanduser(os.getenv("XDG_CACHE_HOME", "~/.cache")), "github_stars"
)
cache_dir = os.path.normpath(cache_dir)
cache_file = os.path.join(cache_dir, "starred_repos")
gap = 4


def get_var(name):
    r = vim.vars.get(name)
    if isinstance(r, bytes):
        return r.decode()
    else:
        return r


username = get_var("leaderf_github_stars_username")
username = username.strip()
assert username is not None
github_token = get_var("leaderf_github_stars_github_token")
maxline = get_var("leaderf_github_stars_maxline") or 100


def parse_lines(lines):
    ret = []
    repos = [(parse_line(line)) for line in lines.split("\n")]
    longest_name = max(repos, key=lambda repo: wcswidth(repo[0]))[0]
    max_name_len = wcswidth(longest_name)
    for name, desc in repos:
        desc_len = maxline - gap - max_name_len
        if desc_len > 0:
            if wcswidth(desc[:desc_len]) > desc_len:
                desc_len = round(desc_len / (wcswidth(desc[:desc_len]) / desc_len))
            ret.append(
                name + (max_name_len + gap - wcswidth(name)) * " " + desc[:desc_len]
            )
        else:
            ret.append(name)
    # lfCmd("echom %r" % len(repos))
    return ret


def parse_line(line):
    line = line.rstrip()
    name, sep, desc = line.partition(" ")
    return (name, desc)
    # name = name[:25]
    # desc = desc[:50].strip()
    # spaces = 30 - wcswidth(name)
    # return name + spaces * ' ' + desc


# *****************************************************
# StarsExplorer
# *****************************************************
class StarsExplorer(Explorer):
    def __init__(self):
        self._repo_list = []
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def getContent(self, *args, **kwargs):
        if not os.path.exists(cache_file):
            return self.getFreshContent()
        elif len(self._repo_list) > 0:
            return self._repo_list
        else:
            self._repo_list = []

            with open(cache_file, "rb") as f:
                self._repo_list = parse_lines(f.read().decode("utf-8"))
            return self._repo_list

    def getFreshContent(self, *args, **kwargs):
        lfCmd("echom 'fetching data from GitHub, it may take a while'")
        self._repo_list = []
        with open(cache_file, "wb") as f:
            page = 0
            while True:
                page += 1

                url = "https://api.github.com/users/%s/starred?per_page=100&page=%d" % (
                    username,
                    page,
                )
                req = Request(url)
                if github_token is not None:
                    req.add_header("Authorization", "token %s" % github_token)
                resp = urlopen(req)

                starred_repos = json.load(resp)
                if len(starred_repos) == 0:
                    break
                lines = "\n".join(
                    [
                        (
                            "%s %s"
                            % (
                                repo["full_name"],
                                ""
                                if repo["description"] is None
                                else repo["description"],
                            )
                        )
                        for repo in starred_repos
                    ]
                )
                f.write(lines.encode("utf-8"))
                self._repo_list = parse_lines(lines)

        return self._repo_list

    def getStlCategory(self):
        return "Stars"

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))

    def isFilePath(self):
        return False


# *****************************************************
# StarsExplManager
# *****************************************************
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
        repo = line.split(" ")[0]
        url = "https://github.com/%s" % repo
        lfCmd("call leaderf#Stars#open('%s')" % url)

    def _getDigest(self, line, mode):
        if not line:
            return ""
        return line

    def _getDigestStartPos(self, line, mode):
        return 0

    def _createHelp(self):
        help = []
        help.append('" <F1> : toggle this help')
        help.append('" <F5> : refresh the cache')
        help.append('" <CR>/<double-click>/o : open repo in browser')
        help.append('" i : switch to input mode')
        help.append('" q : quit')
        help.append('" ---------------------------------------------------------')
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


# *****************************************************
# starsExplManager is a singleton
# *****************************************************
starsExplManager = StarsExplManager()

__all__ = ["starsExplManager"]
