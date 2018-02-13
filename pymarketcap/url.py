#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.error import HTTPError
from urllib.request import urlopen

class Response:
    def __init__(self, text, status_code, url):
        self.text = text
        self.status_code = status_code
        self.url = url

def get_to_memory(url, timeout, debug):
    req = urlopen(url.decode(), timeout=timeout)
    data = req.read()
    res = Response(data, req.getcode(), url)
    req.close()
    return res
