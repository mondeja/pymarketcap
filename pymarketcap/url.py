# -*- coding: utf-8 -*-

"""Urllib implementation for pymarketcap."""

from urllib.error import HTTPError
from urllib.request import urlopen, Request

from pymarketcap import __version__

class Response:
    """Internal response object for encapsulate responses
    getted by requests with urllib module."""
    def __init__(self, text, status_code, url):
        self.text = text
        self.status_code = status_code
        self.url = url

def get_to_memory(url, timeout, debug):
    """GET request stored in memory.

    Args:
        timeout (int): Number of seconds until
            expiration time cancels the request.
        debug (bool): See code response or not.
    """
    req = Request(
        url.decode(),
        headers={"User-Agent": "pymarketcap %s" % __version__}
    )
    try:
        req = urlopen(req, timeout=timeout)
    except HTTPError as err:
        return Response(b"", err.code, url)
    else:
        data = req.read()
        if debug:
            print(data)
        res = Response(data, req.getcode(), url)
        req.close()
        return res
