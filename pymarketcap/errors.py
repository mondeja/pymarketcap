#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Pymarketcap errors module"""

from requests.exceptions import HTTPError

class CoinmarketcapError(Exception):
    """Coinmarketcap base classs errors"""
    pass


                    # HTTP Errors #

class CoinmarketcapHTTPError(HTTPError, CoinmarketcapError):
    """
    Exception for catch 500s range code responses.

    Args:
       code (str): Exception error code.
       msg (str): Human readable string describing the exception.
    """
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
        super().__init__(code, msg)

class CoinmarketcapTooManyRequestsError(CoinmarketcapHTTPError):
    """Exception for catch 429 HTTP error codes"""
    def __init__(self, code, msg):
        super(CoinmarketcapHTTPError, self).__init__(code, msg)


                    # Value Errors #
class CoinmarketcapCurrencyNotFoundError(ValueError, CoinmarketcapError):
    """
    Exception for catch invalid currency parameters as
    function values.

    Args:
        msg (str): Error message displayed
    """
    def __init__(self, currency, url):
        self.currency = currency
        self.url = url
        self.curr_msg = "Currency %s not exists" % currency
        self.url_msg = "%s not found" % url
        super().__init__(self.curr_msg, self.url_msg)
