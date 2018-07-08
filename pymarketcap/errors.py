# -*- coding: utf-8 -*-

"""Pymarketcap errors module."""

class CoinmarketcapError(Exception):
    """Coinmarketcap base classs errors."""
    pass

                    # HTTP Errors #

class CoinmarketcapHTTPError(CoinmarketcapError):
    """Exception for catch HTTPErrors."""
    pass

class CoinmarketcapHTTPError404(CoinmarketcapError):
    """Exception for catch 404 HTTP error codes."""
    pass

class CoinmarketcapHTTPError408(CoinmarketcapError):
    """Exception for catch request timeout HTTP errors."""
    pass

class CoinmarketcapTooManyRequestsError(CoinmarketcapHTTPError):
    """Exception for catch 429 HTTP error codes."""
    pass
